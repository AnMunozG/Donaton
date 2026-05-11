import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";
import { useEffect } from "react";

export default function RichTextEditor({ content, onChange, placeholder }) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({ placeholder: placeholder || "Escribe aquí..." }),
    ],
    content: content || "",
    onUpdate: ({ editor: ed }) => {
      if (onChange) onChange(ed.getHTML());
    },
  });

  useEffect(() => {
    if (editor && content !== editor.getHTML()) {
      editor.commands.setContent(content || "", false);
    }
  }, [content, editor]);

  if (!editor) return null;

  const isActive = (name, attrs) => editor.isActive(name, attrs);
  const toggle = (fn) => editor.chain().focus()[fn]().run();

  const Button = ({ active, onClick, title, children, disabled }) => (
    <button
      type="button"
      className={`btn btn-sm rte-btn ${active ? "btn-secondary" : "btn-outline-secondary"}`}
      onClick={onClick}
      disabled={disabled}
      title={title}
    >
      {children}
    </button>
  );

  return (
    <div className="b-card rounded overflow-hidden">
      <div className="rte-toolbar">
        <Button active={isActive("bold")} onClick={() => toggle("toggleBold")} title="Negrita">
          <strong>B</strong>
        </Button>
        <Button active={isActive("italic")} onClick={() => toggle("toggleItalic")} title="Cursiva">
          <em>I</em>
        </Button>
        <Button active={isActive("strike")} onClick={() => toggle("toggleStrike")} title="Tachado">
          <s>S</s>
        </Button>
        <span className="rte-separator">|</span>
        <Button active={isActive("heading", { level: 2 })} onClick={() => toggle("toggleHeading", { level: 2 })} title="Título H2">
          H2
        </Button>
        <Button active={isActive("paragraph")} onClick={() => toggle("setParagraph")} title="Párrafo">
          P
        </Button>
        <span className="rte-separator">|</span>
        <Button active={isActive("bulletList")} onClick={() => toggle("toggleBulletList")} title="Lista viñetas">
          • Lista
        </Button>
        <Button active={isActive("orderedList")} onClick={() => toggle("toggleOrderedList")} title="Lista numerada">
          1. Lista
        </Button>
        <span className="rte-separator">|</span>
        <Button onClick={() => toggle("undo")} disabled={!editor.can().chain().focus().undo().run()} title="Deshacer">
          ↩
        </Button>
        <Button onClick={() => toggle("redo")} disabled={!editor.can().chain().focus().redo().run()} title="Rehacer">
          ↪
        </Button>
      </div>
      <div className="rte-content">
        <EditorContent editor={editor} />
      </div>
      <style>{`
        .ProseMirror { outline: none; min-height: 100px; }
        .ProseMirror p { margin: 0 0 0.5rem 0; }
        .ProseMirror ul, .ProseMirror ol { padding-left: 1.5rem; }
        .ProseMirror h2 { font-size: 1.25rem; margin: 1rem 0 0.5rem 0; font-weight: 600; }
        .ProseMirror p.is-editor-empty:first-child::before { 
          color: #adb5bd; content: attr(data-placeholder); float: left; height: 0; pointer-events: none; 
        }
      `}</style>
    </div>
  );
}
