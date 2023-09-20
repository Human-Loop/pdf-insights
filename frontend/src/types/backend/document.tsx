export enum BackendDocumentType {
  TenK = "10-K",
  TenQ = "10-Q",
  Lpa = "lpa",
}

export interface BackendDocument {
  created_at: string;
  id: string;
  updated_at: string;
  metadata_map: BackendMetadataMap;
  url: string;
}

export interface BackendMetadataMap {
  sec_document: BackendSecDocument;
  lpa_document: BackendLpaDocument;
}

export interface BackendSecDocument {
  company_name: string;
  company_ticker: string;
  doc_type: BackendDocumentType;
  year: number;
  quarter: number;
}

export interface BackendLpaDocument {
  fund_name: string;
  doc_type: BackendDocumentType;
  company_ticker: string;
  year: number;
}
