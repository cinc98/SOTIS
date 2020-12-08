<template>
  <v-container>
    <d3-network
      :net-nodes="nodes"
      @node-click="clickNode"
      @link-click="clickLink"
      :net-links="links"
      :options="options"
    />
    <v-text-field label="Node name" outlined v-model="nodeName"></v-text-field>
    <v-btn color="success" @click="addNode"> add node </v-btn>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn @click="deleteNode" color="error" dark v-bind="attrs" v-on="on">
          delete node
        </v-btn>
      </template>
      <span>select the node you want to delete</span>
    </v-tooltip>
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
    deleteNode() {
      if (this.clickedNode !== null) {
        this.nodes = this.nodes.filter((n) => n !== this.clickedNode);
        this.links = this.links.filter((l) => l.sid !== this.clickedNode.id);
        this.links = this.links.filter((l) => l.tid !== this.clickedNode.id);
        this.clickedNode = null;
      }
    },
    addNode() {
      this.nodes.push({ name: this.nodeName });
      this.nodeName = null;
    },
    clickNode(event, node) {
      if (this.clickedNode === null) {
        this.clickedNode = node;
        node._color = "green";
      } else {
        this.links.push({ sid: this.clickedNode.id, tid: node.id });
        this.nodes.find((x) => x.id === this.clickedNode.id)._color = "";
        this.clickedNode = null;
      }
    },
    clickLink(event, link) {
      this.links = this.links.filter((l) => l !== link);
    },
  },
  data() {
    return {
      nodeName: null,
      clickedNode: null,
      nodes: [
        { id: 1 },
        { id: 2 },
        { id: 3 },
        { id: 4 },
        { id: 5 },
        { id: 6 },
        { id: 7 },
        { id: 8 },
        { id: 9 },
      ],
      links: [
        { sid: 1, tid: 2 },
        { sid: 2, tid: 8 },
        { sid: 3, tid: 4 },
        { sid: 4, tid: 5 },
        { sid: 5, tid: 6 },
        { sid: 7, tid: 8 },
        { sid: 5, tid: 8 },
        { sid: 3, tid: 8 },
        { sid: 7, tid: 9 },
      ],
      nodeSize: 30,
      canvas: false,
    };
  },
  computed: {
    options() {
      return {
        force: 3000,
        size: { w: 600, h: 600 },
        nodeSize: this.nodeSize,
        nodeLabels: true,
        linkLabels: true,
        canvas: this.canvas,
      };
    },
  },
};
</script>

<style src="vue-d3-network/dist/vue-d3-network.css"></style>
