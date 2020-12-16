<template>
  <v-dialog v-model="show"  persistent width="1000px">
    <v-card  >
      <h2>Knowledge Space: {{ this.$store.state.ksTitle }}</h2>
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
        :net-links="links"
        :options="options"
        :link-cb="lcb"
      />
      <v-btn color="blue darken-1" text @click="dialogToggle">Close</v-btn>
    </v-card>
  </v-dialog>
</template>

<script>
import D3Network from "vue-d3-network";
import axios from "axios";

export default {
  name: "GraphView",
  components: {
    D3Network,
  },
  props: ["dialogToggle", "show", "nodes", "links"],
  data() {
    return {
      containerWidth: 0,
      nodeSize: 20,
      canvas: false,
    };
  },
  methods: {
    lcb(link) {
      link._svgAttrs = {
        "marker-end": "url(#m-end)",
      };
      return link;
    },
  },
  computed: {
    calculateHeightAndWidth() {
      this.containerWidth = this.$refs.graphCard.clientWidth;
    },
    options() {
      return {
        force: 3000,
        size: { w: 1000, h: 700 },
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