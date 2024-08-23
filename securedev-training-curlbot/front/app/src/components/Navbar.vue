<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 50px;">
    <a class="navbar-brand" href="/">CurlBot <span class="badge badge-danger">BETA</span></a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div  class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav" v-show="isAuthenticated">
        <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Profile' }">Profile</router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Bots' }">My Bots</router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'PublicBots' }">Search Bot</router-link>
        </li>
        <li class="nav-item">
            <button type="button" class="btn btn-danger" @click.prevent="Logout">Logout</button>
        </li>
        </ul>
    </div>
    </nav>
</template>
<script>
import axios from 'axios'
import store from '../store/AuthenticationStore'
export default {
    methods: {
        Logout(){
            axios.get("/api/v1/auth/logout",{withCredentials: true})
            .then(
            response => {
                if(response.data.status=="success"){
                    store.commit('LOGOUT');
                }
            })
        }
    },
    computed:{
        isAuthenticated: function(){
            return store.getters.isAuthenticated;
        }
    }
}
</script>