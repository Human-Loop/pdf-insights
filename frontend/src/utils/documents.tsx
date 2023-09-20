import type { LpaDocument, Ticker, DocumentType } from "~/types/document";
import { SelectOption } from "~/types/selection";

export function getAllTickers(documents: LpaDocument[]): Ticker[] {
  const result: Ticker[] = [];
  const seen: { [key: string]: boolean } = {};

  for (const doc of documents) {
    console.log(doc)
    // Skip if we've seen this ticker before
    if (seen[doc.ticker]) {
      continue;
    }

    seen[doc.ticker] = true;
    result.push({
      fullName: doc.fullName,
      ticker: doc.ticker,
    });
  }

  return result;
}

export function filterByTickerAndType(
  ticker: string,
  docType: DocumentType,
  documents: LpaDocument[]
): LpaDocument[] {
  if (!ticker) {
    return [];
  }
  return documents.filter(
    (document) => document.ticker === ticker && document.docType === docType
  );
}

export function findDocumentById(
  id: string,
  documents: LpaDocument[]
): LpaDocument | null {
  return documents.find((val) => val.id === id) || null;
}

export function sortDocuments(selectedDocuments: LpaDocument[]): LpaDocument[] {
  return selectedDocuments.sort((a, b) => {
    // Sort by fullName
    const nameComparison = a.fullName.localeCompare(b.fullName);
    if (nameComparison !== 0) return nameComparison;

    // If fullNames are equal, sort by year
    return a.year.localeCompare(b.year);
  });
}

export function sortSelectOptions(
  options: SelectOption[] | null = []
): SelectOption[] {
  if (!options) {
    return [];
  }

  return options.sort((a, b) => parseInt(a.label) - parseInt(b.label));
}
