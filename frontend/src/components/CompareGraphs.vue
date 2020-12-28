<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card ref="graphCard" outlined>
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
        </v-card>
      </v-col>
      <v-col>
        <v-card outlined>
          <h2>Knowledge Space: {{ this.$store.state.ksTitle }} - Real</h2>
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
            :net-nodes="nodesReal"
            :net-links="linksReal"
            :options="options"
            :link-cb="lcb"
          />
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col align="center">
        <v-card outlined>
          <h2>Comparison</h2>
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
            :net-nodes="nodesReal"
            :net-links="linksCompare"
            :options="options"
            :link-cb="lcb"
          />
          <v-chip id="expected" class="ma-2" > Expected </v-chip>
          <v-chip id="real" class="ma-2" > Real </v-chip>
          <v-chip id="both" class="ma-2" > Both contain </v-chip>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import D3Network from "vue-d3-network";
import axios from "axios";

export default {
  name: "CompareGraphs",
  components: {
    D3Network,
  },
  data() {
    return {
      nodes: [],
      links: [],
      nodesReal: [],
      linksReal: [],
      linksCompare: [],
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
  created() {
    axios
      .all([
        axios.get(`http://localhost:5000/ks/${this.$store.state.ksTitle}`, {
          headers: {
            Authorization: sessionStorage.getItem("token"),
          },
        }),
        axios.get(
          `http://localhost:5000/ks/${this.$store.state.ksTitle} - Real`,
          {
            headers: {
              Authorization: sessionStorage.getItem("token"),
            },
          }
        ),
      ])
      .then(
        axios.spread((data1, data2) => {
          this.nodes = data1.data.knowledge_space.problems;
          this.links = data1.data.knowledge_space.links;
          this.nodesReal = data2.data.knowledge_space.problems;
          this.linksReal = data2.data.knowledge_space.links;
          var vm = this;

          this.nodes.forEach(function (n) {
            vm.nodesReal.forEach(function (nr) {
              if (nr.name === n.name) {
                vm.linksReal.forEach(function (l) {
                  if (l.sid === nr.id) {
                    l.sid = n.id;
                  }
                  if (l.tid === nr.id) {
                    l.tid = n.id;
                  }
                });
                nr.id = n.id;
              }
            });
          });

          this.links.forEach(function (lin) {
            var uso = false;
            vm.linksReal.forEach(function (ln) {
              if (lin.sid === ln.sid && lin.tid === ln.tid) {
                uso = true;

                vm.linksCompare.push({
                  sid: ln.sid,
                  tid: ln.tid,
                  _color: "green",
                });
              }
            });
            if (!uso) {
              vm.linksCompare.push({
                sid: lin.sid,
                tid: lin.tid,
                _color: "blue",
              });
            }
          });

          this.linksReal.forEach(function (ln) {
            var exists = vm.linksCompare.some(
              (elem) => elem.sid === ln.sid && elem.tid === ln.tid
            );
            if (!exists) {
              vm.linksCompare.push({
                sid: ln.sid,
                tid: ln.tid,
                _color: "red",
              });
            }
          });
        })
      );
  },
  computed: {
    calculateHeightAndWidth() {
      this.containerWidth = this.$refs.graphCard.clientWidth;
    },
    options() {
      return {
        force: 3000,
        size: { w: this.containerWidth, h: 400 },
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

<style>
#expected{
    background-color: blue !important;
    color: white;
}
#real{
    background-color: red !important;
    color: white;
}
#both{
    background-color: green !important;
    color: white;
}
</style>