import Vuex from 'vuex'
import router from '../router'

const state = {
    login: undefined,
}

const mutations = {
    LOGIN: (state,login) => {
        state.login = login;
        router.push("/profile", () => {});
    },
    LOGOUT: (state) => {
        state.login = undefined;
        router.push("/login", () => {});
    },
}
const getters = {
    isAuthenticated: state => state.login != undefined,
}

export default new Vuex.Store({
    state: state,
    mutations: mutations,
    getters: getters,
    actions: {},
    strict: true,
})