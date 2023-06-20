<script setup>
import * as echarts from 'echarts';
import {onMounted} from "vue";

onMounted(() => {
  drawGraph()
})

function drawGraph() {
  var myChart = echarts.init(document.getElementById('echarts_container'));
  myChart.setOption({
    legend: [{  //图例组件

    }],
    tooltip: {  //提示框组件

    },
    series: [{
      type: 'graph',
      layout: 'none',

      data: graph.nodes,
      links: graph.links,
      categories: graph.categories,

      emphasis: {  //高亮状态的图形样式
        focus: 'adjacency',  //聚焦关系图中的邻接点和边的图形
        lineStyle: {
          width: 5
        }
      },
      roam: true,  //开启鼠标缩放和平移漫游
      draggable: true,  //设置节点可拖拽
      scaleLimit: {  //滚轮缩放的极限控制
        min: 1,
        max: 10
      },

      label: {  //图形上的文本标签
        show: true,
        position: 'inside',
      },
      labelLayout: {  //标签的统一布局配置
        hideOverlap: true  //缩放时自动隐藏标签
      },

      edgeSymbol: ['none', 'arrow'],  //边两端的标记类型，设置为箭头
      edgeLabel: {  //边标签配置
        show: true,
      },
      lineStyle: {  //边的公用线条样式
        color: 'source'
      }

    }]
  });
}

</script>

<template>
  <div id="echarts_container" style="width: 600px;height:400px;"></div>
</template>

<style scoped>

</style>