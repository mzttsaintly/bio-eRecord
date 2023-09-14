<template>
    <nut-tabs v-model="materialTabsStates">
        <nut-tab-pane title="物料信息查询">
            <el-scrollbar :height="'80vh'">
                <el-table :data="severData">
                    <el-table-column prop="id" label="ID" sortable></el-table-column>
                    <el-table-column prop="material_name" label="物料名称" sortable :filters="filtersName"
                        :filter-method="filterNameMethod">
                        <template v-slot="editRow">
                            <span v-show="editRow.row.id !== editIndex">{{ editRow.row.material_name }}</span>
                            <el-input v-show="editRow.row.id === editIndex" v-model="editRow.row.material_name"></el-input>
                        </template>
                    </el-table-column>

                    <el-table-column prop="material_lot" label="物料批号" sortable>
                        <template v-slot="editRow">
                            <span v-show="editRow.row.id !== editIndex">{{ editRow.row.material_lot }}</span>
                            <el-input v-show="editRow.row.id === editIndex" v-model="editRow.row.material_lot"></el-input>
                        </template>
                    </el-table-column>

                    <el-table-column label="有效期/复验期" sortable>
                        <template v-slot="editRow">
                            <span v-show="editRow.row.id !== editIndex">{{ editRow.row.material_EOV }}</span>
                            <el-input v-show="editRow.row.id === editIndex" v-model="editRow.row.material_EOV"></el-input>
                        </template>
                    </el-table-column>

                    <el-table-column label="操作">
                        <template v-slot="operation_material">
                            <el-button @click="handleEdit(operation_material.row)">
                                <el-icon>
                                    <EditPen v-show="operation_material.row.id !== editIndex" />
                                    <Select v-show="operation_material.row.id === editIndex"></Select>
                                </el-icon>
                            </el-button>

                            <el-tooltip content="删除条目">
                                <el-button type="danger" @click="verifyDelMaterial(operation_material.row.id)"><el-icon>
                                        <CloseBold />
                                    </el-icon></el-button>
                            </el-tooltip>
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </nut-tab-pane>

        <nut-tab-pane title="物料信息录入">
            <el-button @click="pushMaterial" type="info">提交</el-button>
            <el-scrollbar :height="'60vh'">
                <el-form :model="addMaterial">
                    <el-form-item v-for="(item, index) in addMaterial" :key="index">
                        <el-tag>{{ index + 1 }}</el-tag>
                        <el-input v-model="item.material_name"><template #prepend>物料名称</template></el-input>
                        <el-input v-model="item.material_lot"><template #prepend>物料批号</template></el-input>
                        <el-input v-model="item.material_EOV"><template #prepend>有效期/复验期</template></el-input>
                    </el-form-item>
                </el-form>
            </el-scrollbar>
            <el-button type="primary" @click="addM">+</el-button>
        </nut-tab-pane>
    </nut-tabs>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import baseUrl from '../assets/apilink.json'

import { useLoginStore } from '../stores/counter';
import { ElMessageBox } from 'element-plus';
import type { AxiosError, AxiosResponse } from 'axios';

// 从服务器获得token
const tokenStore = useLoginStore()
// 生成的请求头
const gotHeaders = tokenStore.get_headers()

// 声明物料信息类型
interface Material {
    material_name: string;
    material_lot: string;
    material_EOV: string;
}

const addMaterial: Material[] = reactive([{
    material_name: ref(''),
    material_lot: ref(''),
    material_EOV: ref('')
}])

const addM = () => {
    addMaterial.push({
        material_name: ref('').value,
        material_lot: ref('').value,
        material_EOV: ref('').value
    })
}

// 提交数据
const addMaterialUrl = baseUrl['baseUrl'] + 'material/add'

const pushMaterial = () => {
    axios.post(addMaterialUrl, addMaterial, gotHeaders).then(
        (response: AxiosResponse) => {
            ElMessageBox.alert(response.data, '提交结果', {
                confirmButtonText: 'OK',
            })
            getSeverData()
        }
    ).catch((err: AxiosError) => {
        ElMessageBox.alert(err.message, '服务器错误', {
            confirmButtonText: 'OK',
        })
        console.log(err)
    })
}

// 选项卡参数
const materialTabsStates = ref(0)

// 获取物料列表链接
const getMaterialUrl = baseUrl['baseUrl'] + 'material/get_all'

// 临时存储从服务器获取的数据
const severData: rowInfo[] = reactive([])

// 从服务器获取数据
const getSeverData = async () => {
    await axios.get(getMaterialUrl).then(
        (response: AxiosResponse) => {
            severData.length = 0;
            response.data.forEach((item: rowInfo) => {
                severData.push(item)
            })
            // severData = response.data;
            // console.log(severData)
        }
    ).catch((err: AxiosError) => {
        ElMessageBox.alert(err.message, '服务器错误', {
            confirmButtonText: 'OK',
        })
        console.log(err)
    })
}

// 删除条目
const del_url = baseUrl['baseUrl'] + 'material/del'

// 删除前确认
const verifyDelMaterial = async (id: number) => {
    ElMessageBox.confirm('确定删除该条目？', '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(
        async () => {
            await delMaterial(id)
        }
    )
}

const delMaterial = async (id: number) => {
    await axios.post(del_url, { 'del_id': id }, gotHeaders).then(
        (response: AxiosResponse) => {
            ElMessage(response.data)
        }
    ).catch((err: AxiosError) => {
        console.log(err)
        ElMessage(err.message)
    })
    await getSeverData()
}

onMounted(async () => {
    await getSeverData()
    getFiltersName()
})

// 需编辑的行所在的index
const editIndex = ref(-1)

// 声明row的格式
interface rowInfo {
    id: number;
    material_name: string;
    material_lot: string;
    material_EOV: string
}

// 设置将要编辑的行index
const handleEdit = async (row: rowInfo) => {
    if (editIndex.value !== row.id) {
        editIndex.value = row.id
    } else {
        let tempInfo: rowInfo = {
            id: row.id,
            material_name: row.material_name,
            material_lot: row.material_lot,
            material_EOV: row.material_EOV
        }
        ElMessageBox.confirm(`物料名称:${tempInfo.material_name},物料批号:${tempInfo.material_lot},有效期/复验期:${tempInfo.material_EOV}`, '确认修改', {
            confirmButtonText: '是',
            cancelButtonText: '否',
            type: 'warning',
        }).then(async () => {
            console.log(tempInfo)
            await modifyMaterial(tempInfo)
            await getSeverData()
        }).catch(async () => {
            await getSeverData()
        })
        editIndex.value = -1

    }

}

// 修改条目
const modifyUrl = baseUrl['baseUrl'] + 'material/update'

const modifyMaterial = async (modifyInfo: rowInfo) => {
    await axios.post(modifyUrl, modifyInfo, gotHeaders).then((response: AxiosResponse) => {
        ElMessage(response.data)
    }).catch((err: AxiosError) => {
        console.log(err.message)
        ElMessage(err.message)
    })
}

// 名称筛选方法
const filterNameMethod = (value: string, row: rowInfo) => {
    return row.material_name === value
}

// 获取名称排序filters数组
const filtersName: object[] = reactive([])

const getFiltersName = () => {
    const uniquerFilrersName = new Map()

    severData.forEach((item: rowInfo) => {
        uniquerFilrersName.set(item.material_name, 1)
    })

    uniquerFilrersName.forEach((value, key) => {
        filtersName.push({
            text: key,
            value: key
        })
    })
}
</script>