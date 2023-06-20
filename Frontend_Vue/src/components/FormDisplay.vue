<script>

</script>

<template>
    <el-descriptions
            class="kg_info_form"
            title="结点信息"
            :column="1"
            :size="size"
            border
    >
        <el-descriptions-item>
            <template #label>
                <div class="cell-item">
                    Name
                </div>
            </template>
            {{"  "}}
        </el-descriptions-item>
        <el-descriptions-item>
            <template #label>
                <div class="cell-item">
                    Info
                </div>
            </template>
            {{"  "}}
        </el-descriptions-item>
        <el-descriptions-item>
            <template #label>
                <div class="cell-item">
                    Page
                </div>
            </template>
            {{"  "}}
        </el-descriptions-item>
        <el-descriptions-item>
            <template #label>
                <div class="cell-item">
                    Link
                </div>
            </template>
            {{"  "}}
        </el-descriptions-item>
    </el-descriptions>
</template>

<style>

</style>