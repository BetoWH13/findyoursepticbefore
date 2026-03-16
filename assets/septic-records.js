/* ==========================================
Septic Records Search Tool
Repo-ready version based on the standalone
state records finder prototype
========================================== */

document.addEventListener("DOMContentLoaded", function () {
  const stateSelect = document.getElementById("stateSelect");
  const addressInput = document.getElementById("addressInput");
  const searchButton = document.getElementById("recordsSearchButton");
  const resultBox = document.getElementById("searchResult");
  const statesGrid = document.getElementById("statesGrid");
  const noResults = document.getElementById("noResults");
  const resultsCount = document.getElementById("resultsCount");
  const sectionTitle = document.getElementById("sectionTitle");

  if (!stateSelect || !statesGrid) return;

  const STATES = [
    { name: "Alabama", abbr: "AL", slug: "alabama", agency: "Alabama Department of Public Health", tags: ["address", "county"], url: "https://www.alabamapublichealth.gov/environmental/onsite-sewage.html" },
    { name: "Alaska", abbr: "AK", slug: "alaska", agency: "Alaska DEC – On-Site Water & Wastewater", tags: ["address", "county"], url: "https://dec.alaska.gov/eh/drinking-water/on-site-wastewater/" },
    { name: "Arizona", abbr: "AZ", slug: "arizona", agency: "Arizona Dept of Environmental Quality – OSSF", tags: ["address", "county"], url: "https://www.azdeq.gov/ossf" },
    { name: "Arkansas", abbr: "AR", slug: "arkansas", agency: "Arkansas Dept of Health – Onsite Wastewater", tags: ["address", "county"], url: "https://www.healthy.arkansas.gov/programs-services/topics/onsite-wastewater" },
    { name: "California", abbr: "CA", slug: "california", agency: "CA State Water Board – Onsite Wastewater (OWTS)", tags: ["address", "county"], url: "https://www.waterboards.ca.gov/water_issues/programs/owts/" },
    { name: "Colorado", abbr: "CO", slug: "colorado", agency: "Colorado Dept of Public Health – OWTS", tags: ["address", "county"], url: "https://cdphe.colorado.gov/onsite-wastewater-treatment-systems" },
    { name: "Connecticut", abbr: "CT", slug: "connecticut", agency: "CT DEEP – Subsurface Sewage Disposal", tags: ["address", "county"], url: "https://portal.ct.gov/DEEP/Water/Septic-Systems/Septic-Systems" },
    { name: "Delaware", abbr: "DE", slug: "delaware", agency: "Delaware Dept of Natural Resources – OSWC", tags: ["address", "county"], url: "https://dnrec.delaware.gov/water/wastewater/onsite/" },
    { name: "Florida", abbr: "FL", slug: "florida", agency: "Florida Dept of Health – Onsite Sewage Programs", tags: ["address", "county"], url: "https://www.floridahealth.gov/environmental-health/onsite-sewage/index.html" },
    { name: "Georgia", abbr: "GA", slug: "georgia", agency: "Georgia Dept of Public Health – Environmental Health", tags: ["address", "county"], url: "https://dph.georgia.gov/environmental-health/septage-management" },
    { name: "Hawaii", abbr: "HI", slug: "hawaii", agency: "Hawaii Dept of Health – Wastewater Branch", tags: ["address", "county"], url: "https://health.hawaii.gov/wastewater/" },
    { name: "Idaho", abbr: "ID", slug: "idaho", agency: "Idaho Dept of Environmental Quality – Septic", tags: ["address", "county"], url: "https://www.deq.idaho.gov/water-quality/wastewater/septic-systems/" },
    { name: "Illinois", abbr: "IL", slug: "illinois", agency: "Illinois EPA – Private Sewage Disposal", tags: ["address", "county"], url: "https://epa.illinois.gov/topics/water-quality/private-sewage-disposal-systems.html" },
    { name: "Indiana", abbr: "IN", slug: "indiana", agency: "Indiana Dept of Health – Residential Onsite Sewage", tags: ["address", "county"], url: "https://www.in.gov/health/eid/residential-onsite-sewage-systems/" },
    { name: "Iowa", abbr: "IA", slug: "iowa", agency: "Iowa DNR – Private Sewage Disposal", tags: ["address", "county"], url: "https://www.iowadnr.gov/Environmental-Protection/Water-Quality/Wastewater/Private-Sewage" },
    { name: "Kansas", abbr: "KS", slug: "kansas", agency: "Kansas Dept of Health & Environment – Wastewater", tags: ["address", "county"], url: "https://www.kdhe.ks.gov/1390/Wastewater" },
    { name: "Kentucky", abbr: "KY", slug: "kentucky", agency: "Kentucky Division of Water – Onsite Sewage", tags: ["address", "county"], url: "https://eec.ky.gov/Environmental-Protection/Water/Wastewater/Pages/Onsite-Sewage.aspx" },
    { name: "Louisiana", abbr: "LA", slug: "louisiana", agency: "Louisiana Dept of Health – Sewage Disposal", tags: ["address", "county"], url: "https://ldh.la.gov/page/sewage" },
    { name: "Maine", abbr: "ME", slug: "maine", agency: "Maine Dept of Health – Plumbing & HSHC", tags: ["address", "county"], url: "https://www.maine.gov/dhhs/mecdc/environmental-health/plumbing/" },
    { name: "Maryland", abbr: "MD", slug: "maryland", agency: "Maryland MDE – Onsite Disposal Systems", tags: ["address", "county"], url: "https://mde.maryland.gov/programs/water/wateringestionandcommunication/pages/ods.aspx" },
    { name: "Massachusetts", abbr: "MA", slug: "massachusetts", agency: "MassDEP – Septic Systems (Title 5)", tags: ["address", "county"], url: "https://www.mass.gov/septic-systems-title-5" },
    { name: "Michigan", abbr: "MI", slug: "michigan", agency: "Michigan EGLE – Onsite Water & Sewage", tags: ["address", "county"], url: "https://www.michigan.gov/egle/about/organization/water-resources/onsite-water-and-sewage" },
    { name: "Minnesota", abbr: "MN", slug: "minnesota", agency: "Minnesota PCA – Septic Systems (SSTS)", tags: ["address", "county"], url: "https://www.pca.state.mn.us/water/septic-systems" },
    { name: "Mississippi", abbr: "MS", slug: "mississippi", agency: "Mississippi Dept of Health – On-Site Wastewater", tags: ["address", "county"], url: "https://msdh.ms.gov/page/44,0,76.html" },
    { name: "Missouri", abbr: "MO", slug: "missouri", agency: "Missouri Dept of Health – On-Site Wastewater", tags: ["address", "county"], url: "https://health.mo.gov/living/environment/onsite/" },
    { name: "Montana", abbr: "MT", slug: "montana", agency: "Montana DEQ – Septic & Subsurface Sewage", tags: ["address", "county"], url: "https://deq.mt.gov/water/wastewaterbasics/subsurfacesewage" },
    { name: "Nebraska", abbr: "NE", slug: "nebraska", agency: "Nebraska Dept of Environment & Energy – OSSF", tags: ["address", "county"], url: "https://dee.ne.gov/dee.nsf/Pages/OSSF" },
    { name: "Nevada", abbr: "NV", slug: "nevada", agency: "Nevada Division of Environmental Protection – Septic", tags: ["address", "county"], url: "https://ndep.nv.gov/water/wastewater-and-septic/septic-systems" },
    { name: "New Hampshire", abbr: "NH", slug: "new-hampshire", agency: "NH DES – Subsurface Systems Bureau", tags: ["address", "county"], url: "https://www.des.nh.gov/water/wastewater/septic" },
    { name: "New Jersey", abbr: "NJ", slug: "new-jersey", agency: "NJ DEP – Onsite Wastewater Management", tags: ["address", "county"], url: "https://www.nj.gov/dep/wastewater/septic.html" },
    { name: "New Mexico", abbr: "NM", slug: "new-mexico", agency: "NM Environment Dept – Liquid Waste Bureau", tags: ["address", "county"], url: "https://www.env.nm.gov/drinking_water/liquid-waste-bureau/" },
    { name: "New York", abbr: "NY", slug: "new-york", agency: "NY DEC – Septic & Onsite Wastewater", tags: ["address", "county"], url: "https://www.dec.ny.gov/chemical/8791.html" },
    { name: "North Carolina", abbr: "NC", slug: "north-carolina", agency: "NC Dept of Health – On-Site Water Protection", tags: ["address", "county"], url: "https://ehs.ncpublichealth.com/oswp/" },
    { name: "North Dakota", abbr: "ND", slug: "north-dakota", agency: "North Dakota Dept of Environmental Quality – Septic", tags: ["address", "county"], url: "https://www.deq.nd.gov/wm/onsite.aspx" },
    { name: "Ohio", abbr: "OH", slug: "ohio", agency: "Ohio EPA – Household Sewage Treatment Systems", tags: ["address", "county"], url: "https://epa.ohio.gov/divisions-and-offices/surface-water/permits/household-sewage-treatment-systems" },
    { name: "Oklahoma", abbr: "OK", slug: "oklahoma", agency: "Oklahoma Dept of Environmental Quality – OSSF", tags: ["address", "county"], url: "https://www.deq.ok.gov/wqd/ossf/" },
    { name: "Oregon", abbr: "OR", slug: "oregon", agency: "Oregon DEQ – Onsite Wastewater Systems", tags: ["address", "county"], url: "https://www.oregon.gov/deq/wq/onsite/Pages/default.aspx" },
    { name: "Pennsylvania", abbr: "PA", slug: "pennsylvania", agency: "PA Dept of Environmental Protection – OSTS", tags: ["address", "county"], url: "https://www.dep.pa.gov/Business/Water/CleanWater/WastewaterMgmt/SepticSystems/Pages/default.aspx" },
    { name: "Rhode Island", abbr: "RI", slug: "rhode-island", agency: "RI Dept of Health – ISDS (Individual Sewage Disposal)", tags: ["address", "county"], url: "https://health.ri.gov/water/detail.php?id=196" },
    { name: "South Carolina", abbr: "SC", slug: "south-carolina", agency: "SC Dept of Health & Environmental Control – Septic", tags: ["address", "county"], url: "https://scdhec.gov/environment/water-pollution-control/septic-systems-onsite-wastewater" },
    { name: "South Dakota", abbr: "SD", slug: "south-dakota", agency: "South Dakota DENR – Septic Tank Permits", tags: ["address", "county"], url: "https://danr.sd.gov/water-rights/other-water-programs/septic-tank/" },
    { name: "Tennessee", abbr: "TN", slug: "tennessee", agency: "TN Dept of Environment & Conservation – Onsite Wastewater", tags: ["address", "county"], url: "https://www.tn.gov/environment/program-areas/wr-water-resources/onsite-wastewater.html" },
    { name: "Texas", abbr: "TX", slug: "texas", agency: "Texas Commission on Environmental Quality – OSS", tags: ["address", "county"], url: "https://www.tceq.texas.gov/permitting/wastewater/onsite/" },
    { name: "Utah", abbr: "UT", slug: "utah", agency: "Utah Dept of Environmental Quality – Onsite Wastewater", tags: ["address", "county"], url: "https://deq.utah.gov/water-quality/onsite-wastewater" },
    { name: "Vermont", abbr: "VT", slug: "vermont", agency: "Vermont DEC – Wastewater System & Potable Water Supply", tags: ["address", "county"], url: "https://dec.vermont.gov/water-investment/wastewater" },
    { name: "Virginia", abbr: "VA", slug: "virginia", agency: "Virginia Dept of Health – Onsite Sewage & Water", tags: ["address", "county"], url: "https://www.vdh.virginia.gov/drinking-water/onsite-sewage-water-services/" },
    { name: "Washington", abbr: "WA", slug: "washington", agency: "WA Dept of Health – On-Site Sewage (OSS)", tags: ["address", "county"], url: "https://doh.wa.gov/community-and-environment/wastewater/on-site-sewage-systems" },
    { name: "West Virginia", abbr: "WV", slug: "west-virginia", agency: "WV Dept of Health – Environmental Engineering", tags: ["address", "county"], url: "https://dhhr.wv.gov/bph/environmentalengineering/Pages/default.aspx" },
    { name: "Wisconsin", abbr: "WI", slug: "wisconsin", agency: "Wisconsin DNR – Private On-Site Wastewater Treatment", tags: ["address", "county"], url: "https://dnr.wisconsin.gov/topic/Wastewater/onsite" },
    { name: "Wyoming", abbr: "WY", slug: "wyoming", agency: "Wyoming DEQ – Septic Systems", tags: ["address", "county"], url: "https://deq.wyoming.gov/wqd/wastewater/septic-systems/" }
  ];

  function populateDropdown() {
    const placeholder = stateSelect.querySelector('option[value=""]');
    stateSelect.innerHTML = "";
    if (placeholder) {
      stateSelect.appendChild(placeholder);
    } else {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "— All States —";
      stateSelect.appendChild(option);
    }

    STATES.forEach((state) => {
      const option = document.createElement("option");
      option.value = state.abbr;
      option.textContent = `${state.name} (${state.abbr})`;
      stateSelect.appendChild(option);
    });
  }

  function tagClass(tag) {
    return {
      address: "tag-address",
      county: "tag-county",
      owner: "tag-owner",
      parcel: "tag-parcel"
    }[tag] || "tag-address";
  }

  function tagLabel(tag) {
    return {
      address: "Address",
      county: "County",
      owner: "Owner Name",
      parcel: "Parcel #"
    }[tag] || tag;
  }

  function renderSummaryCard(state) {
    if (!resultBox || !state) return;

    resultBox.innerHTML = `
      <div class="state-result">
        <h3>${state.name} septic records</h3>
        <p>${state.agency}</p>
        <p>This page links to the main state-level agency. If your county manages septic permits locally, the next step is usually the county health department or environmental health office.</p>
        <p><a href="${state.url}" target="_blank" rel="noopener noreferrer">Open ${state.name} records resource</a></p>
      </div>
    `;
  }

  function clearSummaryCard() {
    if (resultBox) {
      resultBox.innerHTML = "";
    }
  }

  function renderCards(list) {
    if (!statesGrid || !noResults || !resultsCount) return;

    statesGrid.innerHTML = "";

    if (!list.length) {
      noResults.style.display = "block";
      resultsCount.textContent = "0 results";
      return;
    }

    noResults.style.display = "none";
    resultsCount.textContent = `${list.length} state${list.length !== 1 ? "s" : ""}`;

    list.forEach((state) => {
      const card = document.createElement("article");
      card.className = "state-card";

      card.innerHTML = `
        <div class="card-top">
          <div class="state-name">${state.name}</div>
          <span class="state-abbr">${state.abbr}</span>
        </div>
        <div class="agency-name">${state.agency}</div>
        <div class="search-types">
          ${state.tags.map((tag) => `<span class="tag ${tagClass(tag)}">${tagLabel(tag)}</span>`).join("")}
        </div>
        <a class="visit-btn" href="${state.url}" target="_blank" rel="noopener noreferrer" aria-label="Open ${state.name} septic records resource">
          Search ${state.abbr} Records
        </a>
      `;

      statesGrid.appendChild(card);
    });
  }

  function doSearch() {
    const enteredAddress = addressInput ? addressInput.value.trim() : "";
    const selectedAbbr = stateSelect.value;
    let filtered = STATES;

    if (selectedAbbr) {
      filtered = STATES.filter((state) => state.abbr === selectedAbbr);
    }

    if (sectionTitle) {
      if (selectedAbbr && enteredAddress) {
        sectionTitle.textContent = `State resource for "${enteredAddress}" in ${selectedAbbr}`;
      } else if (selectedAbbr) {
        sectionTitle.textContent = `Septic records — ${filtered[0]?.name || selectedAbbr}`;
      } else if (enteredAddress) {
        sectionTitle.textContent = `State resources for "${enteredAddress}"`;
      } else {
        sectionTitle.textContent = "All State Databases";
      }
    }

    if (filtered.length === 1) {
      renderSummaryCard(filtered[0]);
    } else {
      clearSummaryCard();
    }

    renderCards(filtered);
  }

  populateDropdown();
  renderCards(STATES);

  stateSelect.addEventListener("change", doSearch);

  if (searchButton) {
    searchButton.addEventListener("click", doSearch);
  }

  if (addressInput) {
    addressInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        doSearch();
      }
    });
  }
});
