<template>
    <div>
      <a class="hiddenanchor" id="signup"></a>
      <a class="hiddenanchor" id="signin"></a>

      <div class="login_wrapper">
        <div class="animate form login_form">
          <section class="login_content">
            <form>
              <h1>Reset your password</h1>
              <h3>Asks for a reset token</h3>
              <div v-show="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>
              <div v-show="success" class="alert alert-success" role="alert">
                {{ success }}
              </div>
              <div class="form-group">
                <input v-model="login" type="text" class="form-control" placeholder="Username" required="" />
              </div>
              <input type="submit" class="btn btn-success" @click.prevent="GetReset" value="Get Token"/>
              <hr>
              <div class="form-group">
                <input v-model="token" class="form-control" placeholder="Reset Token" required="" />
              </div>
              <div class="form-group">
                <input v-model="password" type="password" class="form-control" placeholder="New Password" required="" />
              </div>
              
              <input type="submit" class="btn btn-success" @click.prevent="Reset" value="Change Password"/>
              <hr>
              <router-link to="login" class="btn btn-primary" style="margin-right: 5px">Login</router-link>
              <router-link to="register" class="btn btn-primary">Create an Account</router-link>
              

            </form>
          </section>
        </div>
      </div>
    </div>
</template>
<script>
import axios from 'axios'
import store from '../store/AuthenticationStore'
export default {
    store: store,
    data: function () {
      return {
        login: undefined,
        password: undefined,
        token: undefined,
        error: undefined,
        success: undefined,
        role: "user"
      }
    },
    methods: {
      Reset(){
          if(this.token && this.password){
            var that = this;
            axios.post("/api/v1/auth/reset-password",
            {
              password: that.password,
              token: that.token,
            },{withCredentials: true}).then(
            response => {
                that.error = undefined;
                if(response.data.status=="error"){
                    that.error = response.data.message;
                }
                else if(response.data.status=="success"){
                    that.success = response.data.message;
                }
            })
            .catch(function(error) {
              if (error.response && error.response.status === 401) {
                that.error = error.response.data.message;
              }
            })
          }
        },
      GetReset(){
          if(this.login){
            var that = this;
            axios.post("/api/v1/auth/reset",
            {
              login: that.login,
            },{withCredentials: true}).then(
            response => {
                that.error = undefined;
                if(response.data.status=="error"){
                    that.error = response.data.message;
                }
                else if(response.data.status=="success"){
                    that.success = response.data.message;
                }
            })
            .catch(function(error) {
              if (error.response && error.response.status === 401) {
                that.error = error.response.data.message;
              }
            })
          }
        }
    }
}
</script>
