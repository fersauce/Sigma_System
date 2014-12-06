//
//  main.js
//
//  A project template for using arbor.js
//

(function($){
  $(document).ready(function(){
        var graph = new joint.dia.Graph;

        var paper = new joint.dia.Paper({
            el: $('#paper'),
            width: 2000,
            height: 2000,
            model: graph,
            gridSize: 1
        });

        function makeElement(label) {
            var maxLineLength = _.max(label.split('\n'), function(l) { return l.length; }).length;
            // Compute width/height of the rectangle based on the number
            // of lines in the label and the letter size. 0.6 * letterSize is
            // an approximation of the monospace font letter width.
            var letterSize = 8;
            var width = 2 * (letterSize * (0.6 * maxLineLength + 1));
            var height = 2 * ((label.split('\n').length + 1) * letterSize);
            return new joint.shapes.basic.Rect({
                id: label,
                size: { width: width, height: height },
                attrs: {
                    text: { text: label, 'font-size': letterSize, 'font-family': 'monospace' },
                    rect: {
                        width: width, height: height,
                        rx: 5, ry: 5,
                        stroke: '#555'
                    }
                }
            });
        }

        function makeLink(parentElementLabel, childElementLabel) {
            return new joint.dia.Link({
                source: { id: parentElementLabel },
                target: { id: childElementLabel },
                attrs: { '.marker-target': { d: 'M 4 0 L 0 2 L 4 4 z' } },
                smooth: true
            });
        }

        function buildGraphFromAdjacencyList(adjacencyList) {
            var elements = [];
            var links = [];

            _.each(adjacencyList, function(edges, parentElementLabel) {
                elements.push(makeElement(parentElementLabel));

                _.each(edges, function(childElementLabel) {
                    links.push(makeLink(parentElementLabel, childElementLabel));
                });
            });

            // Links must be added after all the elements. This is because when the links
            // are added to the graph, link source/target
            // elements must be in the graph already.
            return elements.concat(links);
        }

        var lista_ady = {   'T': ['b', 'c'],
                            'b': ['f'],
                            'c': ['e', 'd'],
                            'd': [],
                            'e': [],
                            'f': ['g'],
                            'g': []
                        }
        l =  {'T':['b','c']};

        var cells = buildGraphFromAdjacencyList(l);
        graph.resetCells(cells);

        //joint.layout.DirectedGraph.layout(graph, { setLinkVertices: false });


        /*var rect = new joint.shapes.basic.Rect({
            position: { x: 100, y: 30 },
            size: { width: 100, height: 30 },
            attrs: { rect: { fill: 'blue' }, text: { text: 'my box', fill: 'white' } }
        });

        var rect2 = rect.clone();
        rect2.translate(300);

        var link = new joint.dia.Link({
            source: { id: rect.id },
            target: { id: rect2.id }
        });

        graph.addCells([rect, rect2, link]);*/

  })

})(this.jQuery)