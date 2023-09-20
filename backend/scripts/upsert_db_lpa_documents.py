from pathlib import Path
from fire import Fire
from tqdm import tqdm
import asyncio
from pytickersymbols import PyTickerSymbols
from file_utils import get_available_files
from fastapi.encoders import jsonable_encoder
from app.models.db import Document
from app.schema import (
    SecDocumentMetadata,
    DocumentMetadataMap,
    DocumentMetadataKeysEnum,
    SecDocumentTypeEnum,
    Document,
)
from app.db.session import SessionLocal
from app.api import crud

DEFAULT_URL_BASE = "https://dl94gqvzlh4k8.cloudfront.net"
DEFAULT_DOC_DIR = "data/"


async def upsert_document(doc_dir: str, lpa: str, url_base: str):
    # construct a string for just the document's sub-path after the doc_dir
    # e.g. "sec-edgar-filings/AAPL/10-K/0000320193-20-000096/filing-details.pdf"
    doc_path = Path(lpa).relative_to(doc_dir)
    url_path = url_base.rstrip("/") + "/" + str(doc_path).lstrip("/")
    doc_type = 'lpa'    

    lpa_doc_metadata = LpaDocumentMetadata(
        fund_name=lpa,
        doc_type=doc_type,
    )
    metadata_map: DocumentMetadataMap = {
        DocumentMetadataKeysEnum.LPA_DOCUMENT: jsonable_encoder(
            lpa_doc_metadata.dict(exclude_none=True)
        )
    }
    doc = Document(url=str(url_path), metadata_map=metadata_map)
    async with SessionLocal() as db:
        await crud.upsert_document_by_url(db, doc)


async def async_upsert_documents_from_files(url_base: str, doc_dir: str):
    """
    Upserts SEC documents into the database based on what has been downloaded to the filesystem.
    """
    files = get_available_files(doc_dir)
    print(f"Files: {files}")
    for file in tqdm(files, desc="Upserting docs from files"):
        await upsert_document(doc_dir, file, url_base)


def main_upsert_documents_from_files(
    url_base: str = DEFAULT_URL_BASE, doc_dir: str = DEFAULT_DOC_DIR
):
    """
    Upserts SEC documents into the database based on what has been downloaded to the filesystem.
    """

    asyncio.run(async_upsert_documents_from_files(url_base, doc_dir))


if __name__ == "__main__":
    Fire(main_upsert_documents_from_files)
