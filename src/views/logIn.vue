<template>
    <nut-cell class="loginWindow">
        <el-form ref="userFormRef" :model="userForm">
            <el-form-item label="用户名：" prop="username">
                <el-input v-model="userForm.username" clearable @keyup.enter="() => passwordInput.focus()"></el-input>
            </el-form-item>
            <el-form-item label="密码：" prop="password">
                <el-input ref="passwordInput" type="password" v-model="userForm.password" clearable
                    @keyup.enter="login"></el-input>
            </el-form-item>
            <nut-button type="default" @click="resetForm(userFormRef)">清空</nut-button>
            <nut-button type="success" @click="login">登录</nut-button>
        </el-form>

    </nut-cell>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useLoginStore } from '../stores/counter';
import axios from 'axios';
import baseUrl from '../assets/apilink.json';
import { useRouter } from 'vue-router'

import type { FormInstance } from 'element-plus'
const router = useRouter()
// 保存的token
const tokenStore = useLoginStore()
// 输入的登录数据
const userForm = reactive({
    username: ref<string>(''),
    password: ref<string>('')
})

// 表单对象代理
const userFormRef = ref<FormInstance>()

// 密码框对象代理
const passwordInput = ref()

// 重置表单项
const resetForm = (form1: FormInstance | undefined) => {
    if (!form1) return
    form1.resetFields()
}

// 登录获取token
const login_url = baseUrl['baseUrl'] + 'login'

const FormHeader = {
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
}

const login = () => {
    axios.post(login_url, userForm, FormHeader).then(
        (response) => {
            let res_access_token = response.data.access_token
            let res_token_type = response.data.token_type
            let res = res_token_type + " " + res_access_token
            // console.log(res)
            tokenStore.changeToken(res)
            router.push({ path: '/userInfo' })
        }
    ).catch((err) => {
        ElMessageBox.alert(err.response.data, '发生错误', {
            confirmButtonText: 'OK',
        })
        console.log(err)
    })
}
</script>

<style scoped>
.loginWindow {
    justify-content: center;
}
</style>