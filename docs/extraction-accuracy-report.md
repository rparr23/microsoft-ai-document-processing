# Extraction evaluation status

No live AI Builder extraction was run. The three normalized extraction fixtures were authored from the synthetic invoice ground truth. Their confidence values are demonstration inputs; they are not model measurements. Therefore no OCR accuracy percentage is reported.

For an actual evaluation, process held-out PDFs through the published model, capture model/version, raw output and normalization, then compare each required value to sample-data/ground-truth.json after agreed normalization. Report exact field matches / evaluated fields, document-level all-fields-correct rate, low-confidence review rate, unreadable cases and duplicates separately. Include training/test separation and cost/latency. The fixture suite tests downstream validation, not extraction quality.
