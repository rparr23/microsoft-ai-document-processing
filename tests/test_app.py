import copy
import json
import unittest
from pathlib import Path
from src.app import connect, process, review, validate

ROOT = Path(__file__).resolve().parents[1]


class DocumentTests(unittest.TestCase):
    def setUp(self):
        self.db = connect(':memory:')
        self.doc = json.loads((ROOT/'sample-data/extraction-1.json').read_text())

    def tearDown(self):
        self.db.close()

    def test_valid_fields_require_approval(self):
        result = process(self.db, self.doc)
        self.assertEqual(result['state'], 'pending_approval')
        self.assertEqual(result['values']['total'], '1250.00')
        self.assertEqual(review(self.db, 'doc-1', 'approve', 'synthetic-reviewer')['state'], 'approved')

    def test_missing_value_and_low_confidence(self):
        self.doc['fields']['total'] = {'value': None, 'confidence': 0.1}
        result = process(self.db, self.doc)
        self.assertIn('missing:total', result['issues'])
        self.assertIn('low_confidence:total', result['issues'])
        with self.assertRaises(ValueError):
            review(self.db, 'doc-1', 'approve', 'reviewer')

    def test_invalid_money_date_currency(self):
        for key, value in [('total','NaN'), ('total','-1'), ('total','1.001'), ('invoice_date','2026-02-30'), ('currency','XXX')]:
            doc = copy.deepcopy(self.doc)
            doc['fields'][key]['value'] = value
            self.assertTrue(validate(doc)[1])

    def test_malformed_confidence(self):
        for confidence in [float('nan'), float('inf'), -1, 2, True, 'high']:
            self.doc['fields']['total']['confidence'] = confidence
            with self.assertRaises(ValueError):
                validate(self.doc)

    def test_duplicate_invoice_normalization(self):
        process(self.db, self.doc)
        self.doc['document_id'] = 'doc-2'
        self.doc['fields']['vendor']['value'] = ' CONTOSO   Supplies '
        self.assertIn('duplicate_invoice', process(self.db, self.doc)['issues'])

    def test_retry_and_conflicting_upload(self):
        process(self.db, self.doc)
        self.assertTrue(process(self.db, self.doc)['duplicate_upload'])
        self.doc['fields']['total']['value'] = '99.00'
        with self.assertRaises(ValueError):
            process(self.db, self.doc)

    def test_rejected_reservation_can_be_replaced(self):
        process(self.db, self.doc)
        review(self.db, 'doc-1', 'reject', 'reviewer')
        self.doc['document_id'] = 'doc-1-v2'
        self.assertEqual(process(self.db, self.doc)['state'], 'pending_approval')

    def test_review_decision_is_recorded_and_final(self):
        process(self.db, self.doc)
        review(self.db, 'doc-1', 'approve', 'reviewer')
        self.assertEqual(self.db.execute('SELECT reviewer FROM documents').fetchone()[0], 'reviewer')
        with self.assertRaises(ValueError):
            review(self.db, 'doc-1', 'reject', 'reviewer')


if __name__ == '__main__':
    unittest.main()
