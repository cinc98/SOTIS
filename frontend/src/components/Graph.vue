<template>
  <v-container ref="graphContainer">
    <h2>Create graph</h2>
        <v-text-field label="KS Title" outlined v-model="ksTitle"></v-text-field>

    <svg>
      <defs>
        <marker
          id="m-end"
          markerWidth="10"
          markerHeight="10"
          refX="15"
          refY="3"
          orient="auto"
          markerUnits="strokeWidth"
        >
          <path d="M0,0 L0,6 L9,3 z"></path>
        </marker>
      </defs>
    </svg>
    <d3-network
      :net-nodes="nodes"
      @node-click="clickNode"
      @link-click="clickLink"
      :net-links="links"
      :options="options"
      :link-cb="lcb"
    />
    <v-text-field label="Node name" outlined v-model="nodeName"></v-text-field>
    <v-row justify="end">
      <v-col>
        <v-btn color="success" @click="addNode"> add node </v-btn>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              @click="deleteNode"
              color="error"
              dark
              v-bind="attrs"
              v-on="on"
            >
              delete node
            </v-btn>
          </template>
          <span>select the node you want to delete</span>
        </v-tooltip>
      </v-col>
      <v-col class="text-right" >
        <v-btn color="primary" @click="saveGraph"> save graph </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import D3Network from "vue-d3-network";

export default {
  name: "Graph",
  components: {
    D3Network,
  },
  methods: {
    lcb(link) {
      link._svgAttrs = {
        "marker-end": "url(#m-end)",
      };
      return link;
    },
    checkCyclic(sid, tid) {
      var vm = this;
      var isCyclic = false;
      this.links.forEach(function (l) {
        if (l.tid === sid) {
          if (l.sid === tid) {
            vm.isCyclic = true;
          } else {
            vm.checkCyclic(l.sid, tid);
          }
        }
      });
    },
    deleteNode() {
      if (this.clickedNode !== null) {
        this.nodes = this.nodes.filter((n) => n !== this.clickedNode);
        this.links = this.links.filter((l) => l.sid !== this.clickedNode.id);
        this.links = this.links.filter((l) => l.tid !== this.clickedNode.id);
        this.clickedNode = null;
      }
    },
    saveGraph(){
      console.log(this.ksTitle);
      console.log(this.links);
      console.log(this.nodes);

    },
    addNode() {
      this.nodes.push({ id: this.lastNodeId + 1, name: this.nodeName });
      this.lastNodeId++;
      this.nodeName = null;
    },
    clickNode(event, node) {
      if (this.clickedNode === null) {
        this.clickedNode = node;
        node._color = "green";
      } else {
        if (this.clickedNode === node) {
          this.nodes.find((x) => x.id === node.id)._color = "";
          this.clickedNode = null;
          this.isCyclic = false;
        } else {
          this.checkCyclic(this.clickedNode.id, node.id);

          if (!this.isCyclic) {
            this.links.push({ sid: this.clickedNode.id, tid: node.id });
            this.nodes.find((x) => x.id === this.clickedNode.id)._color = "";
            this.clickedNode = null;
            this.isCyclic = false;
          }
        }
      }
    },
    clickLink(event, link) {
      this.links = this.links.filter((l) => l !== link);
    },
  },
  data() {
    return {
      isCyclic: false,
      ksTitle:null,
      containerWidth: 0,
      nodeName: null,
      clickedNode: null,
      lastNodeId: 8,
      nodes: [],
      links: [],
      nodeSize: 20,
      canvas: false,
    };
  },
  computed: {
    calculateHeightAndWidth() {
      this.containerWidth = this.$refs.graphContainer.clientWidth;
    },
    options() {
      return {
        force: 3000,
        size: { w: this.containerWidth, h: 500 },
        nodeSize: this.nodeSize,
        nodeLabels: true,
        linkLabels: true,
        canvas: this.canvas,
        linkWidth: 2,
      };
    },
  },
};
</script>

<style src="vue-d3-network/dist/vue-d3-network.css">
path {
  fill: none;
}
</style>
