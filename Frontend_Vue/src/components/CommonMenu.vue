<script lang="ts" setup>
import {House, ChatLineSquare} from '@element-plus/icons-vue'
import {useRouter} from "vue-router";
import {reactive} from "vue";

const router = useRouter()
const state = reactive({
    currentPath: '/kg'
})

router.beforeEach((to, from, next) => {
    next();
    state.currentPath = to.path;
})
</script>

<template>
    <div class="title">
        <img src="../assets/logo.svg">
        <span>课程知识图谱</span>
    </div>
    <el-menu
        class="menu"
        text-color="#ecf5ff"
        background-color="#2d2e36"
        :default-active="state.currentPath"
        router
    >
        <el-menu-item index="/kg">
            <el-icon><House /></el-icon>
            <span class="menu_title">知识图谱</span>
        </el-menu-item>
        <el-menu-item index="/qa">
            <el-icon><ChatLineSquare /></el-icon>
            <span class="menu_title">智能问答</span>
        </el-menu-item>
    </el-menu>
</template>

<style>
.title {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60px;
}
.title img {
    width: 35px;
    height: 35px;
    margin-right: 10px;
}
.title span {
    font-family: 'Microsoft YaHei';
    font-size: 18px;
    font-weight: bold;
    color: #ecf5ff;
}
.menu_title{
    font-family: 'PingFang SC';
    font-weight: bold;
}
.menu .el-menu-item:hover {
    background-color:#FFFFFF80;
}
.menu .el-menu-item.is-active {
    background-color: #1661ab !important;
    color: #ecf5ff !important;
}
</style>