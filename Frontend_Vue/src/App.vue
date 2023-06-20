<script setup>
    import CommonMenu from "./components/CommonMenu.vue"
</script>

<template>
    <el-container class="container">
        <el-aside class="aside">
            <CommonMenu />
        </el-aside>
        <el-container>
            <el-header class="header" />
            <el-main class="main">
                <router-view />
            </el-main>
        </el-container>
    </el-container>
</template>

<style>
@import "./assets/style/common.scss";
.container{
    height: 100vh;
}
.aside{
    width: 15% !important;
    background-color: #2d2e36;
}
.header{
    background-color: white;
    box-shadow: var(--el-box-shadow-lighter);
}
.main{
    background-color: #f4f8fb;
}
</style>