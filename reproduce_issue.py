import marko
from marko.ext.gfm import GFM
from marko.inline import RawText
from marko.block import Document, Heading

markdown = marko.Markdown(extensions=[GFM])

def test_render():
    print("Creating Nested Structure...")

    # RawText
    rt = RawText.__new__(RawText)
    rt.children = "Updated Test Note"

    # Heading
    h = Heading.__new__(Heading)
    h.level = 1
    h.children = [rt]

    # Document
    doc = Document.__new__(Document)
    doc.children = [h]

    print("Rendering...")
    try:
        output = markdown.render(doc)
        print(f"Output: {output}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_render()
