define('pie-chart', ['double-dollar'], function($$) {
    'use strict';

    function drawPies() {
        $$('.pie').forEach(function(pie) {
            var p = parseFloat(pie.textContent);
            var NS = "http://www.w3.org/2000/svg";
            var svg = document.createElementNS(NS, "svg");
            var circle = document.createElementNS(NS, "circle");
            var title = document.createElementNS(NS, "title");
            circle.setAttribute("r", 16);
            circle.setAttribute("cx", 16);
            circle.setAttribute("cy", 16);
            circle.setAttribute("stroke-dasharray", p + " 100");
            svg.setAttribute("viewBox", "0 0 32 32");
            title.textContent = pie.textContent;
            pie.textContent = '';
            svg.appendChild(title);
            svg.appendChild(circle);
            pie.appendChild(svg);
        });
    }

    return {
        drawPies: drawPies
    }
});
