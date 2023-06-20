<script setup>
import { Position, Refresh } from '@element-plus/icons-vue'
import axios from "axios"
import {ref} from 'vue'

let query = ref('')
let session_log = ref([
  {type: "reply", msg: "欢迎使用知识问答助手！请输入您的问题，我会尽全力帮您解答。"}
])

function submitQuery() {
  let dialog_query = {}
  dialog_query.type = "query"
  dialog_query.msg = query.value
  session_log.value.push(dialog_query)

  axios({
    method: 'post',
    url: 'http://localhost:5000/api/kbqa',
    headers: {'Content-Type': 'application/json'},
    data: {
      query: query.value
    }
  })
      .then(function (response) {
        if (response.status === 200) {
          console.log(response.data)
          let dialog_reply = {}
          dialog_reply.type = "reply"
          dialog_reply.msg = response.data['reply']
          session_log.value.push(dialog_reply)
        }
      })
      .catch(function (error) {
        if (error.response) {
          // 请求成功发出且服务器也响应了状态码，但状态代码超出了 2xx 的范围
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          // 请求已经成功发起，但没有收到响应
          // `error.request` 在浏览器中是 XMLHttpRequest 的实例，
          // 而在node.js中是 http.ClientRequest 的实例
          console.log(error.request);
        } else {
          // 发送请求时出了点问题
          console.log('Error', error.message);
        }
        console.log(error.config);
      })
  query.value = ""
}

function cleanup() {
  session_log.value = [
    {type: "reply", msg: "欢迎使用知识问答助手！请输入您的问题，我会尽全力帮您解答。"}
  ]
}

</script>

<template>
  <el-card class="qa_container">
    <template #header>
      <div class="qa_card_header">
        <span> 知识问答 </span>
      </div>
    </template>
    <div style="margin: 5px 0"/>
    <el-card class="qa_display" shadow="never">
      <el-scrollbar max-height="400px">
        <div v-for="(item, index) in session_log" :key="index">
          <div v-if="item.type === 'query'" >
            <p class="session_query">{{ item.msg }}</p>
          </div>
          <div v-else>
            <p class="session_reply">{{ item.msg }}</p>
          </div>
        </div>
      </el-scrollbar>
    </el-card>
    <div style="margin: 25px 0"/>
    <el-row :gutter="15">
      <el-col :span="20">
        <el-input
            v-model="query"
            type="text"
            size="large"
            maxlength="20"
            show-word-limit
            placeholder="请在此输入您的问题，按回车键提交"
            @keyup.enter="submitQuery"
        />
      </el-col>
      <el-col :span="4">
        <el-button
            type="primary"
            size="large"
            :icon="Position"
            @click="submitQuery">提交</el-button>
        <el-button
            type="danger"
            size="large"
            :icon="Refresh"
            @click="cleanup">清屏</el-button>
      </el-col>
    </el-row>
  </el-card>
</template>

<style>
.qa_container {
  height: 600px;
}

.qa_card_header {
  font-size: 16px;
  font-weight: bold;
}

.qa_display {
  height: 420px;
}

.session_query {
  max-width: 500px;
  width: fit-content;  /* 根据文字长度，自适应width大小 */
  word-wrap: break-word;  /* 文本溢出后，单词不截断换行 */
  margin: 5px 0 5px auto;  /* 利用 margin-left: auto 实现右对齐 */
  padding: 10px;
  border-radius: 4px;
  background: var(--el-color-primary);
  color: var(--el-color-primary-light-9);
}

.session_reply {
  max-width: 500px;
  width: fit-content;
  word-wrap: break-word;
  margin: 5px 0 5px 0;
  padding: 10px;
  border-radius: 4px;
  background: #e5e5e5;
  color: var(--el-color-black);
}
</style>
