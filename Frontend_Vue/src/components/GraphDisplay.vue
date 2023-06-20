<script setup>
import NeoVis from "neovis.js";
import {onMounted, ref} from "vue";

const graph = ref(null);

onMounted(() => {
    draw();
})

function draw() {
    const config = {
        containerId: "graph",
        neo4j: {
            serverUrl: "bolt://localhost:7687",
            serverUser: "neo4j",
            serverPassword: "15421312z"
        },
        labels: {
            "subject": { label: "name", value: "pagerank"},  //color: "#c990c0"
            "module": { label: "name", value: "pagerank"},   //color: "#f79767"
            "content": { label: "name", value: "pagerank"},  //color: "#57c7e3"
            "detail": { label: "name", value: "pagerank"}    //color: "#f16667"
        },
        relationships: {
            "CONTAIN": { value: "weight" }
        },
        visConfig: {
            nodes: {
                shape: "circle",
                widthConstraint: 150
            },
            edges: { label: "CONTAIN", arrows: "to", color: "#a5abb6" },
            layout: { improvedLayout: true },
            physics: {
                barnesHut: {
                    gravitationalConstant: -4000,
                    centralGravity: 0.1,
                    springLength: 120,
                    avoidOverlap: 0.4
                }
            }
        },
        initialCypher: "MATCH (n)-[r:CONTAIN]->(m) RETURN *"
    }
    const neoViz = new NeoVis(config);
    neoViz._container = graph;
    neoViz.render();
}

</script>

<template>
    <div class="graph_container">
        <div id="graph" ref="graph"></div>
    </div>
</template>

<style scoped>
#graph{
    height: 460px;
}
</style>