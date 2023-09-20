import { MAX_NUMBER_OF_SELECTED_DOCUMENTS } from "~/hooks/useDocumentSelector";
import { BackendDocument, BackendDocumentType } from "~/types/backend/document";
import { LpaDocument, DocumentType } from "~/types/document";
import { documentColors } from "~/utils/colors";

export const fromBackendDocumentToFrontend = (
  backendDocuments: BackendDocument[]
) => {
  const frontendDocs: LpaDocument[] = [];
  console.log("empty frontend docs")
  backendDocuments.filter((d) => "lpa_document" in d.metadata_map).map((backendDoc, index) => {
    const backendDocType = backendDoc.metadata_map.lpa_document.doc_type;
    console.log("backenddoc type")
    const frontendDocType =
      backendDocType === BackendDocumentType.Lpa
        ? DocumentType.Lpa
        : DocumentType.Lpa;
    console.log("frontenddoc type")

    // we have 10 colors for 10 documents
    const colorIndex = index < 10 ? index : 0;
    console.log("colorindex")
    const payload = {
      id: backendDoc.id,
      url: backendDoc.url,
      fullName: backendDoc.metadata_map.lpa_document.fund_name,
      year: backendDoc.metadata_map.lpa_document.year.toString(),
      docType: frontendDocType,
      ticker: backendDoc.metadata_map.lpa_document.company_ticker,
      color: documentColors[colorIndex],
    } as LpaDocument;
    console.log("payload", payload)
    frontendDocs.push(payload);
  });
  return frontendDocs;
};
