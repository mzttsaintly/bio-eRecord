<template>
    <nut-divider>登录信息</nut-divider>
    <nut-cell>
        <el-input v-model="userInfo.user_name" disabled>
            <template #prepend>用户名：</template>
        </el-input>

        <el-input v-model="userInfo.user_authority" disabled>
            <template #prepend>权限等级：</template>
        </el-input>


    </nut-cell>
    <nut-button type="primary" @click="logout">退出登录</nut-button>
    <nut-divider>创建新用户</nut-divider>


    <el-input v-model="newUser.username">
        <template #prepend>用户名：</template>
    </el-input>

    <el-input v-model="newUser.password" show-password>
        <template #prepend>密码：</template>
    </el-input>

    <el-checkbox-group v-model="new_authority">
        <el-checkbox :label="1">写记录</el-checkbox>
        <el-checkbox :label="2">修改物料、设备信息</el-checkbox>
        <el-checkbox :label="4">新增用户</el-checkbox>
    </el-checkbox-group>

    <nut-button type="success" @click="create_user">创建新用户</nut-button>

    {{ new_authority }}
    {{ newUser.authority }}
</template>

<script setup lang="ts">
import { useUserInfoStore, useLoginStore } from '../stores/counter';
import { onMounted, reactive, ref, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'
const router = useRouter()
import baseUrl from '../assets/apilink.json';
// 保存用户信息
const userInfo = useUserInfoStore().userInfo
const tokenStore = useLoginStore()
// 生成的请求头
const gotHeaders = tokenStore.get_headers()
// 获取用户信息
const get_userInfo_url = baseUrl['baseUrl'] + 'user/me/'

const get_userInfo = () => {
    axios.get(get_userInfo_url, gotHeaders).then(
        (response) => {
            console.log(response.data)
            userInfo.user_name = response.data.user_name;
            userInfo.user_authority = response.data.authority;
        }
    )
}

// 退出登录
const logout = () => {
    tokenStore.logout()
    router.push({ path: '/login' })
}

onMounted(() => {
    get_userInfo()
})

// 创建新用户
const new_authority = ref([])

const newUser = reactive({
    username: ref(''),
    password: ref(''),
    authority: computed<number>(() => {
        let res = 0
        new_authority.value.forEach(element => {
            res += element
        });
        return res;
    })
})

const create_user_url = baseUrl['baseUrl'] + 'user/create_user'

const create_user = () => {
    axios.post(create_user_url, newUser, gotHeaders).then(
        (response) => {
            ElMessageBox.alert(response.data, '创建结果', {
            confirmButtonText: 'OK',
        })
        }
    ).catch((err) => {
        ElMessageBox.alert(err.response.data, '发生错误', {
            confirmButtonText: 'OK',
        })
        console.log(err)
    })
}
</script>