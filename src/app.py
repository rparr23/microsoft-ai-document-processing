"""Validate normalized AI Builder extraction fixtures. Does not perform OCR."""
import argparse
import json
import math
import sqlite3
import unicodedata
from datetime import date
from decimal import Decimal, InvalidOperation

FIELDS = {'vendor', 'invoice_number', 'invoice_date', 'currency', 'total', 'purchase_order'}


def validate(doc):
    if not isinstance(doc, dict) or set(doc) != {'document_id', 'fields'} or not isinstance(doc['document_id'], str) or not doc['document_id'].strip():
        raise ValueError('Invalid document envelope')
    fields = doc['fields']
    if not isinstance(fields, dict) or set(fields) != FIELDS:
        raise ValueError('Unexpected field schema')
    values, issues = {}, []
    for name, field in fields.items():
        if not isinstance(field, dict) or set(field) != {'value', 'confidence'}:
            raise ValueError('Each field needs value and confidence')
        value, confidence = field['value'], field['confidence']
        if value is not None and not isinstance(value, str):
            raise ValueError('Normalized values must be strings or null')
        if isinstance(confidence, bool) or not isinstance(confidence, (float, int)) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise ValueError('Invalid confidence')
        values[name] = value.strip() if value else None
        if not values[name]:
            issues.append(f'missing:{name}')
        if confidence < 0.85:
            issues.append(f'low_confidence:{name}')
    try:
        date.fromisoformat(values['invoice_date'] or '')
    except ValueError:
        issues.append('invalid:invoice_date')
    try:
        total = Decimal(values['total'] or '')
        if not total.is_finite() or total <= 0 or total.as_tuple().exponent < -2:
            raise InvalidOperation
    except InvalidOperation:
        issues.append('invalid:total')
    if values['currency'] not in {'USD', 'CAD', 'EUR', 'GBP'}:
        issues.append('unsupported:currency')
    return values, sorted(set(issues))


def connect(path):
    db = sqlite3.connect(path)
    db.execute('CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, payload TEXT NOT NULL, state TEXT NOT NULL, reviewer TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS invoices (vendor TEXT, number TEXT, document_id TEXT, UNIQUE(vendor,number))')
    return db


def vendor_key(value):
    return ' '.join(unicodedata.normalize('NFKC', value).casefold().split())


def process(db, doc):
    values, issues = validate(doc)
    payload = json.dumps(doc, sort_keys=True)
    with db:
        prior = db.execute('SELECT payload,state FROM documents WHERE id=?', (doc['document_id'],)).fetchone()
        if prior:
            if prior[0] != payload:
                raise ValueError('Document ID conflict; corrections require a new version')
            return {'state': prior[1], 'duplicate_upload': True}
        if values['vendor'] and values['invoice_number']:
            key = (vendor_key(values['vendor']), vendor_key(values['invoice_number']))
            duplicate = db.execute('SELECT document_id FROM invoices WHERE vendor=? AND number=?', key).fetchone()
            if duplicate:
                issues.append('duplicate_invoice')
            elif not issues:
                db.execute('INSERT INTO invoices VALUES (?,?,?)', (*key, doc['document_id']))
        state = 'needs_review' if issues else 'pending_approval'
        db.execute('INSERT INTO documents(id,payload,state) VALUES (?,?,?)', (doc['document_id'], payload, state))
    return {'state': state, 'issues': issues, 'values': values, 'duplicate_upload': False}


def review(db, document_id, decision, reviewer):
    if decision not in {'approve', 'reject'} or not isinstance(reviewer, str) or not reviewer.strip():
        raise ValueError('Valid decision and reviewer required')
    with db:
        row = db.execute('SELECT state FROM documents WHERE id=?', (document_id,)).fetchone()
        if not row:
            raise ValueError('Unknown document')
        if row[0] not in {'pending_approval', 'needs_review'}:
            raise ValueError('Review already finalized')
        if decision == 'approve' and row[0] != 'pending_approval':
            raise ValueError('Validation issues must be corrected and submitted as a new version')
        state = 'approved' if decision == 'approve' else 'rejected'
        db.execute('UPDATE documents SET state=?,reviewer=? WHERE id=?', (state, reviewer, document_id))
        if decision == 'reject':
            db.execute('DELETE FROM invoices WHERE document_id=?', (document_id,))
    return {'state': state, 'reviewer': reviewer, 'document_id': document_id}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default='state.db')
    sub = parser.add_subparsers(dest='command', required=True)
    load = sub.add_parser('process')
    load.add_argument('extraction')
    rev = sub.add_parser('review')
    rev.add_argument('--id', required=True)
    rev.add_argument('--decision', choices=['approve', 'reject'], required=True)
    rev.add_argument('--reviewer', required=True)
    args = parser.parse_args()
    try:
        with connect(args.db) as db:
            if args.command == 'process':
                with open(args.extraction) as file:
                    result = process(db, json.load(file))
            else:
                result = review(db, args.id, args.decision, args.reviewer)
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, OSError, sqlite3.Error) as exc:
        parser.exit(2, f'Operation failed: {exc}\n')


if __name__ == '__main__':
    main()
