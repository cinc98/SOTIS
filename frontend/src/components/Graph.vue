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
      <v-col class="text-right">
        <v-btn color="primary" @click="saveGraph"> save graph </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import D3Network from "vue-d3-network";
import axios from "axios";

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
    checkTransitive(sid, tid) {
      var vm = this;
      this.links.forEach(function (l) {
        if (l.sid === sid) {
          if (l.tid === tid) {
            vm.isTransitive = true;
          } else {
            vm.checkTransitive(l.tid, tid);
          }
        }
      });
    },
    deleteLinkTransitive(sid, tid) {
      var vm = this;
      this.links.forEach(function (l) {
        if (l.tid === sid) {
          vm.links.forEach(function (li, index) {
            if (li.tid === tid && li.sid === l.sid) {
              vm.links.splice(index, 1);
            }
          });
          vm.deleteLinkTransitive(l.sid, tid);
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
    saveGraph() {
      var tempLinks = [];
      var tempNodes = [];
      for (let l of this.links.entries()) {
        tempLinks.push({
          source_name: l[1].source.name,
          target_name: l[1].target.name,
        });
      }
      for (let n of this.nodes.entries()) {
        tempNodes.push({ node_name: n[1].name });
      }

      axios
        .post(
          "http://localhost:5000/add-ks",
          {
            ks_title: this.ksTitle,
            domain_title: this.$store.state.domainTitle,
            nodes: tempNodes,
            links: tempLinks,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("token"),
            },
          }
        )
        .then((response) => {
          alert(response.data.message);
          this.links = [];
          this.nodes = [];
          this.ksTitle = "";
        })
        .catch((error) => {
          alert(error);
        });
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
          this.isTransitive = false;
        } else {
          this.checkCyclic(this.clickedNode.id, node.id);
          this.checkTransitive(this.clickedNode.id, node.id);
          if (!this.isCyclic && !this.isTransitive) {
            this.links.push({ sid: this.clickedNode.id, tid: node.id });
            this.deleteLinkTransitive(this.clickedNode.id, node.id);
            this.nodes.find((x) => x.id === this.clickedNode.id)._color = "";
            this.clickedNode = null;
            this.isCyclic = false;
            this.isTransitive = false;
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
      isTransitive: false,
      ksTitle: null,
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
