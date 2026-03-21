from pydentic import Field

from mcp.server.fastmcp import FastMCP

from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return them as a string."  
)
def read_doc_content(doc_id: str = Field(description="The ID of the document to read.")):
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    return docs[doc_id]

@mcp.tool(
    name="edit_doc",
    description="Edit the contents of a document."
)

def edit_document(doc_id: str = Field(description="The ID of the document to edit."), 
                  old_str: str = Field(description="The text to replace.Must match exactly, including whitespace."), 
                  new_str: str = Field(description="The new text to insert in place of the old text.")):

    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
  
@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    return docs[doc_id]

@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(doc_id: str = Field(description="Id of the document to format.")) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.
    The Id of the document to format is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, and other markdown syntax to make the document easier to read. Do not change the content of the document, only add formatting. Return the reformatted document as a string.
    Use the "edit_document" tool to make edits to the document. You can call the tool multiple times to make multiple edits. When you are finished, return the final formatted document as a string. 
    """
    return [base.Message(prompt)]
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
