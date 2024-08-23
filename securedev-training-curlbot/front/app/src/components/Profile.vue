<template>
    <div class="right_col">
        <h3>Profile</h3>
        <div v-show="error" class="alert alert-danger" role="alert">
            {{ error }}
        </div>
        <div v-show="success" class="alert alert-success" role="alert">
            {{ success }}
        </div>
        <hr>
        <img :src="'/profile/pic?file='+avatar" style="height: 50px;border-radius: 50%;margin-right: 50px;">
        <button  class="btn btn-success" @click.prevent="UploadPic">Change avatar</button>
        <input ref="avatar" accept=".png,.jpg,.jpeg" v-on:change="submitPic" id="avatar-form" style="display: none" type="file" class="form-control-file">
        <hr>
        <p>Id: {{ id }}</p>
        <p>Login: {{ login }}</p>
        <p>Role: 
            <span v-if="is_admin" class="badge badge-success">Admin</span>
            <span v-else class="badge badge-info">User</span>
        </p>
        <div v-show="flag" class="alert alert-success" role="alert">
            Here is the flag : {{ flag }}
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import store from '../store/AuthenticationStore'
export default {
    data: function () {
      return {
        login: undefined,
        id: undefined,
        resettoken: undefined,
        flag: undefined,
        is_admin: undefined,
        error: undefined,
        success: undefined,
        reset: false,
        avatar: "avatar.png",
      }
    },
    mounted() {
        var that = this;
        axios.get("/api/v1/user/profile",{withCredentials: true})
        .then(
        response => {
            if(response.data.status=="error"){
                if(store.getters.isAuthenticated){
                    store.commit('LOGOUT');
                }
            }
            else {
                    that.id = response.data.id;
                    that.login = response.data.login;
                    that.is_admin = response.data.is_admin;
                    that.avatar = response.data.avatar;
                    if (that.is_admin) {
                        axios.get("/api/v1/flag",{withCredentials: true})
                        .then(
                        response => {
                            if(response.data.status=="success")
                            {
                                that.flag=response.data.message
                            }
                        })
                        .catch(function() {
                            
                        })
                    }
            }
        })
    },
    methods: {
        Reset(){
            this.reset = true
        },
        UploadPic () {
            document.getElementById('avatar-form').click();
        },
        submitPic () {
            var that = this;
            this.success = undefined;
            this.error = undefined;
            const formData = new FormData();
            formData.append('file', this.$refs.avatar.files[0]);
            const headers = { 'Content-Type': 'multipart/form-data' };
            axios.post('/api/v1/user/avatar', formData, { headers }).then((res) => {
                

                if(res.data.status=="success") {
                    that.success=res.data.message;
                    that.avatar=res.data.avatar
                }
                else that.error=res.data.message
            });
        }
    }
}
</script>