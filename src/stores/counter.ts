import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  return { count, doubleCount, increment }
})

// 侧边导航栏是否打开
export const useSideBarStore = defineStore('sidebar', () => {
  const sideBarState = reactive({
    show: false,
    width: '20%',
    height: '100%'
  })
  function handleClick() {
    sideBarState.show = true
  }
  function changeSideBarWidth(new_width: string) {
    sideBarState.width = new_width
  }

  return { sideBarState, handleClick, changeSideBarWidth }
})

// 保存登录信息
interface tokenHeader {
  headers: {
    'authorization'?: string
    'Content-Type'?: string
  }
}

export const useLoginStore = defineStore('login', () => {
  const userToken = ref('')
  function changeToken(newToken: string) {
    userToken.value = newToken
  }
  function logout() {
    userToken.value = ''
  }
  function get_headers() {
    const temp_headers: tokenHeader = {
      headers: {
        'authorization': userToken.value
      }
    }
    return temp_headers
  }
function get_form_headers() {
  const temp_form_headers: tokenHeader = {
    headers: {
      'authorization': userToken.value,
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }
  return temp_form_headers
}

  function notarizeLogin() {
    return userToken.value !== ''
  }

  return { userToken, changeToken, logout, get_headers, get_form_headers, notarizeLogin }
})

// 保存用户登录信息
export const useUserInfoStore = defineStore('userInfo', () => {
  const userInfo = reactive({
    user_name: ref(''),
    user_authority: ref(0)
  })
  return { userInfo }
})
