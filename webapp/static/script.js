function toggleNavOff() {
    var nav = document.getElementById("dropdown-nav");
    let style = window.getComputedStyle(nav)
    nav.style.display = "none";
}

function toggleNav() {
    var nav = document.getElementById("dropdown-nav");
    let style = window.getComputedStyle(nav)
    if (style.display === "none") {
        nav.style.display = "flex";
    } else {
        nav.style.display = "none";
    }
}

function toggleNavPanel(panel_id) {
    var panel = document.getElementById(panel_id);
    let style = window.getComputedStyle(panel);
    if (style.display === "none") {
        panel.style.display = "grid";
    } else {
        panel.style.display = "none";
    }
}

function toggleActionPanel() {
    var panel = document.getElementById("actions_list");
    style = window.getComputedStyle(panel);
    if (style.display === "none") {
        panel.style.display = "grid";
    } else {
        panel.style.display = "none";
    }
}

function toggleActionAltPanel(panel_id) {
    toggleActionPanel()
    var panel = document.getElementById(panel_id);
    style = window.getComputedStyle(panel);
    if (style.display === "none") {
        panel.style.display = "grid";
    } else {
        panel.style.display = "none";
    }
}

function toggleVehicleDetails(panel_id) {
    console.log(panel_id)
    var panel = document.getElementById(panel_id);
    style = window.getComputedStyle(panel);
    if (style.display === "none") {
        panel.style.display = "grid";
    } else {
        panel.style.display = "none";
    }
}