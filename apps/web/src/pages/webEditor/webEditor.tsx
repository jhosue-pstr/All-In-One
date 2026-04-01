import grapesjs from "grapesjs";
import "grapesjs/dist/css/grapes.min.css";
import "./webEditor.css";
import { useEffect } from "react";

function WebEditor() {
  useEffect(() => {
    const editor = grapesjs.init({
      container: "#gjs",
      height: "100%",
      width: "auto",
      storageManager: false,
      panels: { defaults: [] },
      deviceManager: {
        devices: [
          { name: "Desktop", width: "" },
          { name: "Mobile", width: "320px", widthMedia: "480px" },
          { name: "Tablet", width: "768px", widthMedia: "992px" },
        ],
      },
      blockManager: {
        appendTo: "#blocks",
        blocks: [
          {
            id: "section",
            label: "<b>Section</b>",
            attributes: { class: "gjs-block-section" },
            content: `<section><h1>This is a simple title</h1><div>Lorem ipsum dolor sit amet</div></section>`,
          },
          {
            id: "text",
            label: "Text",
            content: '<div data-gjs-type="text">Insert your text here</div>',
          },
          {
            id: "image",
            label: "Image",
            select: true,
            content: { type: "image" },
            activate: true,
          },

          {
            id: "navbar",
            label: "Navbar",
            content: `<nav style="display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background: #333; color: white;"><div style="font-weight: bold;">Logo</div><div style="display: flex; gap: 20px;"><a href="#" style="color: white; text-decoration: none;">Home</a><a href="#" style="color: white; text-decoration: none;">About</a><a href="#" style="color: white; text-decoration: none;">Contact</a></div></nav>`,
          },
          {
            id: "features",
            label: "Features Grid",
            content: `<section style="padding: 60px 30px;"><h2 style="text-align: center; margin-bottom: 40px;">Our Features</h2><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px;"><div style="text-align: center; padding: 20px;"><h3>Feature 1</h3><p>Description of feature one</p></div><div style="text-align: center; padding: 20px;"><h3>Feature 2</h3><p>Description of feature two</p></div><div style="text-align: center; padding: 20px;"><h3>Feature 3</h3><p>Description of feature three</p></div></div></section>`,
          },
          {
            id: "cta",
            label: "CTA Section",
            content: `<section style="padding: 80px 30px; text-align: center; background: #f5f5f5;"><h2>Ready to get started?</h2><p style="margin: 20px 0 30px;">Join thousands of satisfied customers today</p><button style="padding: 15px 40px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">Sign Up Now</button></section>`,
          },
          {
            id: "footer",
            label: "Footer",
            content: `<footer style="padding: 40px 30px; background: #222; color: #999; text-align: center;"><p>&copy; 2026 Your Company. All rights reserved.</p></footer>`,
          },
          {
            id: "columns",
            label: "2 Columns",
            content: `<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 20px;"><div>Column 1</div><div>Column 2</div></div>`,
          },
          {
            id: "button",
            label: "Button",
            content:
              '<button style="padding: 10px 20px; cursor: pointer;">Click Me</button>',
          },
          {
            id: "divider",
            label: "Divider",
            content:
              '<hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">',
          },
        ],
      },
      layerManager: { appendTo: ".layers-container" },
      styleManager: {
        appendTo: ".styles-container",
        sectors: [
          {
            name: "Dimension",
            open: false,
            buildProps: ["width", "min-height", "padding", "margin"],
          },
          {
            name: "Typography",
            open: true,
            buildProps: [
              "font-family",
              "font-size",
              "font-weight",
              "text-align",
              "color",
            ],
          },
          {
            name: "Background",
            open: false,
            buildProps: ["background-color", "background-image"],
          },
          {
            name: "Border",
            open: false,
            buildProps: ["border", "border-radius"],
          },
          {
            name: "Spacing",
            open: false,
            buildProps: ["margin", "padding"],
          },
        ],
      },
      traitManager: { appendTo: ".traits-container" },
      selectorManager: { appendTo: ".styles-container" },
    });

    editor.Panels.addPanel({
      id: "panel-top",
      el: ".panel__top",
    });

    editor.Panels.addPanel({
      id: "basic-actions",
      el: ".panel__basic-actions",
      buttons: [
        {
          id: "visibility",
          active: true,
          className: "btn-toggle-borders",
          label: "B",
          title: "Toggle Borders",
          command: "sw-visibility",
        },
        {
          id: "export",
          className: "btn-open-export",
          label: "Exp",
          title: "Export Template",
          command: "export-template",
        },
        {
          id: "undo",
          className: "btn-undo",
          label: "↩",
          title: "Undo",
          command(editor: any) {
            editor.UndoManager.undo();
          },
        },
        {
          id: "redo",
          className: "btn-redo",
          label: "↪",
          title: "Redo",
          command(editor: any) {
            editor.UndoManager.redo();
          },
        },
        {
          id: "save",
          className: "btn-save",
          label: "💾",
          title: "Save",
          command: "save",
        },
      ],
    });

    editor.Panels.addPanel({
      id: "panel-devices",
      el: ".panel__devices",
      buttons: [
        {
          id: "device-desktop",
          label: "PC",
          title: "Desktop",
          command: "set-device-desktop",
          active: true,
          togglable: false,
        },
        {
          id: "device-mobile",
          label: "MOBIL",
          title: "Mobile",
          command: "set-device-mobile",
          togglable: false,
        },
        {
          id: "device-tablet",
          label: "T",
          title: "Tablet",
          command: "set-device-tablet",
          togglable: false,
        },
      ],
    });

    editor.Panels.addPanel({
      id: "panel-switcher",
      el: ".panel__switcher",
      buttons: [
        {
          id: "show-blocks",
          active: true,
          label: "Blocks",
          command: "show-blocks",
          togglable: false,
        },
        {
          id: "show-layers",
          active: false,
          label: "Layers",
          command: "show-layers",
          togglable: false,
        },
        {
          id: "show-style",
          active: false,
          label: "Styles",
          command: "show-styles",
          togglable: false,
        },
      ],
    });

    editor.Commands.add("show-blocks", {
      run(editor: any) {
        const blocksEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector("#blocks");
        const layersEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector(".layers-container");
        const stylesEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector(".styles-container");
        const traitsEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector(".traits-container");
        if (blocksEl) blocksEl.style.display = "";
        if (layersEl) layersEl.style.display = "none";
        if (stylesEl) stylesEl.style.display = "none";
        if (traitsEl) traitsEl.style.display = "none";
      },
    });

    editor.Commands.add("show-layers", {
      run(editor: any) {
        const blocksEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector("#blocks");
        const layersEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector(".layers-container");
        const stylesEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector(".styles-container");
        const traitsEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector(".traits-container");
        if (blocksEl) blocksEl.style.display = "none";
        if (layersEl) layersEl.style.display = "";
        if (stylesEl) stylesEl.style.display = "none";
        if (traitsEl) traitsEl.style.display = "none";
      },
    });

    editor.Commands.add("show-styles", {
      run(editor: any) {
        const blocksEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector("#blocks");
        const layersEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector(".layers-container");
        const stylesEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector(".styles-container");
        const traitsEl = editor
          .getContainer()
          .closest(".editor-row")
          .querySelector(".traits-container");
        if (blocksEl) blocksEl.style.display = "none";
        if (layersEl) layersEl.style.display = "none";
        if (stylesEl) stylesEl.style.display = "";
        if (traitsEl) traitsEl.style.display = "none";
      },
    });

    editor.Commands.add("set-device-desktop", {
      run: (editor: any) => editor.setDevice("Desktop"),
    });
    editor.Commands.add("set-device-mobile", {
      run: (editor: any) => editor.setDevice("Mobile"),
    });
    editor.Commands.add("set-device-tablet", {
      run: (editor: any) => editor.setDevice("Tablet"),
    });

    editor.Commands.add("save", {
      run(editor: any) {
        const projectData = editor.getProjectData();
        console.log("Project Data:", projectData);
        const html = editor.getHtml();
        const css = editor.getCss();
        console.log("HTML:", html);
        console.log("CSS:", css);
        localStorage.setItem("gjs-project", JSON.stringify(projectData));
        alert("Project saved!");
      },
    });

    return () => editor.destroy();
  }, []);

  return (
    <div className="editor-container">
      <div className="panel__top">
        <div className="panel__basic-actions" />
        <div className="panel__devices" />
        <div className="panel__switcher" />
      </div>

      <div className="editor-row">
        <div className="editor-canvas">
          <div id="gjs">
            <h1>Hello World Component!</h1>
          </div>
        </div>

        <div className="panel__right">
          <div id="blocks" />
          <div className="layers-container" style={{ display: "none" }} />
          <div className="styles-container" style={{ display: "none" }} />
          <div className="traits-container" style={{ display: "none" }} />
        </div>
      </div>
    </div>
  );
}

export default WebEditor;
