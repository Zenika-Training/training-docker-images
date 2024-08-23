<template>
    <div>
      <a class="hiddenanchor" id="signup"></a>
      <a class="hiddenanchor" id="signin"></a>

      <div class="login_wrapper">
        <div class="animate form login_form">
          <section class="login_content">
            <form>
              <h1>Login</h1>
              <div v-show="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>
              <div v-show="success" class="alert alert-success" role="alert">
                {{ success }}
              </div>
              <div class="form-group">
                <input v-model="login" type="text" class="form-control" placeholder="Username" required="" />
              </div>
              <div class="form-group">
                <input v-model="password" type="password" class="form-control" placeholder="Password" required="" />
              </div>
                <input type="submit" class="btn btn-success" @click.prevent="Login" value="Log in" style="margin-right: 5px"/>
                <router-link to="reset" class="btn btn-primary">Reset your password</router-link>

              <hr>
              <p>New to site ?
                <router-link to="register" class="btn btn-primary">Create an Account</router-link>
              </p>
              <p>Suggest a new feature ?
                <router-link to="contact" class="btn btn-secondary">Contact us</router-link>
              </p>
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
        endpoint:'/api/v1/auth/login',
        error: undefined,
        success: undefined,
        password: undefined,
        login: undefined,
      }
    },
    mounted: function() {
      if(this.$route.query.token!=undefined){
        var that = this;
        axios.get("/api/v1/auth/reset?token="+that.$route.query.token,
        {
            login: that.login,
            password: that.password,
        },{withCredentials: true})
        .then(response => {
            that.error = undefined;
            that.success = undefined;
            if(response.data.status=="error"){
                that.error = response.data.message;
            }
            else if(response.data.status=="success"){
                that.success = "Your password is : "+response.data.message;
            }
        });
      }
    },
    methods: {
        Login(){
            if(this.login && this.password){
                var that = this;
                axios.post("/api/v1/auth/login",
                {
                    login: that.login,
                    password: that.password,
                },{withCredentials: true}).then(
                response => {
                    that.error = undefined;
                    if(response.data.status=="error"){
                        that.error = response.data.message;
                    }
                    else if(response.data.status=="success"){
                        store.commit('LOGIN',that.login);
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
