<script setup>
import FormDisplay from "@/components/FormDisplay.vue";
import GraphDisplay from "@/components/GraphDisplay.vue"
</script>

<template>
    <el-card class="kg_container">
        <template #header>
            <div class="kg_card_header">
                <span> 课程知识图谱 </span>
            </div>
        </template>
        <el-row>
            <el-col :span="18">
                <el-card class="kg_display" shadow="never">
                    <GraphDisplay />
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-card class="kg_info" shadow="never">
                    <FormDisplay />
                </el-card>
            </el-col>
        </el-row>
    </el-card>
</template>

<style>
.kg_container{
    height: 600px;
}
.kg_card_header{
    font-size: 16px;
    font-weight: bold;
}
.kg_display{
    height: 500px;
}
.kg_info{
    height: 500px;
}
</style>