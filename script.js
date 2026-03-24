const btn = document.getElementById("compareBtn");

btn.addEventListener("click", function () {

    const p1 = document.getElementById("proc1").value;
    const p2 = document.getElementById("proc2").value;

    if (!p1 || !p2) {
        alert("Please select both processors");
        return;
    }

    if (p1 === p2) {
        alert("Please select two different processors");
        return;
    }

    // Redirect to compare page with URL parameters
    window.location.href = `compare.html?proc1=${encodeURIComponent(p1)}&proc2=${encodeURIComponent(p2)}`;
});