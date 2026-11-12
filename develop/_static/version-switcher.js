document.addEventListener("DOMContentLoaded", () => {
  for (const selector of document.querySelectorAll(".docs-version-switcher")) {
    const status = selector.parentElement.querySelector(".docs-version-error");
    const manifestUrl = new URL(selector.dataset.manifest, document.baseURI);
    const reportError = (error) => {
      status.textContent = "Could not switch documentation versions. Please reload to retry.";
      status.hidden = false;
      console.error("Documentation version switcher:", error);
    };

    fetch(manifestUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Version manifest returned HTTP ${response.status}`);
        }
        return response.json();
      })
      .then((versions) => {
        for (const entry of versions) {
          const option = document.createElement("option");
          option.textContent = entry.name;
          option.value = new URL(entry.url, manifestUrl).href;
          option.dataset.legacy = String(entry.legacy === true);
          if (entry.version === selector.dataset.version) {
            selector.options[0].remove();
            option.selected = true;
          }
          selector.append(option);
        }
      })
      .catch(reportError);

    selector.addEventListener("change", async () => {
      const option = selector.selectedOptions[0];
      if (!option.value) {
        return;
      }
      if (option.dataset.legacy === "true") {
        window.location.assign(option.value);
        return;
      }
      const pageUrl = new URL(selector.dataset.page, option.value);
      selector.disabled = true;
      try {
        const response = await fetch(pageUrl, { method: "HEAD" });
        if (response.ok) {
          pageUrl.hash = window.location.hash;
          window.location.assign(pageUrl.href);
        } else if (response.status === 404) {
          window.location.assign(option.value);
        } else {
          throw new Error(`Documentation page returned HTTP ${response.status}`);
        }
      } catch (error) {
        reportError(error);
        selector.disabled = false;
      }
    });
  }
});
