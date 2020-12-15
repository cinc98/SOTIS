<template>
  <v-container ref="graphContainer">
    <h2>Knowledge Space: {{this.$store.state.ksTitle}}</h2>
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
  </v-container>
</template>

<script>
import D3Network from "vue-d3-network";
import axios from "axios";

export default {
  name: "GraphView",
  components: {
    D3Network,
  },
  data() {
    return {
      containerWidth: 0,
      nodes: [],
      links: [],
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
  created() {
    axios
      .get(`http://localhost:5000/ks/${this.$store.state.ksTitle}`, {
        headers: {
          Authorization: sessionStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.nodes = response.data.knowledge_space.problems;
        this.links = response.data.knowledge_space.links;
      })
      .catch((error) => {
        this.$router.push("/");
      });
  },
  computed: {
    calculateHeightAndWidth() {
      this.containerWidth = this.$refs.graphContainer.clientWidth;
    },
    options() {
      return {
        force: 3000,
        size: { w: this.containerWidth, h: 700 },
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