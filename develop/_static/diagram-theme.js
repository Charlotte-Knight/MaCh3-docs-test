document.addEventListener("DOMContentLoaded", () => {
  const diagrams = document.querySelectorAll("object.graphviz");
  const update = (diagram) => {
    const svg = diagram.contentDocument?.querySelector("svg");
    if (!svg) {
      return;
    }
    const theme = getComputedStyle(document.documentElement);
    const color = (name) => theme.getPropertyValue(`--pst-color-${name}`).trim();
    let style = svg.querySelector("#mach3-diagram-theme");
    if (!style) {
      style = diagram.contentDocument.createElementNS("http://www.w3.org/2000/svg", "style");
      style.id = "mach3-diagram-theme";
      svg.append(style);
    }
    const dark = document.documentElement.dataset.theme === "dark";
    style.textContent = `
      text { fill: ${color("text-base")}; }
      .node polygon, .node ellipse, .node path {
        fill: ${color("background")};
        stroke: ${color("text-muted")};
      }
      .node [fill="#bfbfbf" i] { fill: ${color("surface")}; }
      .edge [stroke="#1414ce" i] { stroke: ${dark ? "#fff" : "#000"}; }
      .edge [fill="#1414ce" i] { fill: ${dark ? "#fff" : "#000"}; }
      ${dark ? `
        .edge [stroke="#8b1a1a" i] { stroke: #f08080; }
        .edge [fill="#8b1a1a" i] { fill: #f08080; }
        .edge [stroke="#006400" i] { stroke: #80c080; }
        .edge [fill="#006400" i] { fill: #80c080; }
        .edge [stroke="#9c35ce" i] { stroke: #cf90ef; }
        .edge [fill="#9c35ce" i] { fill: #cf90ef; }
      ` : ""}
    `;
  };
  for (const diagram of diagrams) {
    diagram.addEventListener("load", () => update(diagram));
    update(diagram);
  }
  new MutationObserver(() => diagrams.forEach(update)).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
});
