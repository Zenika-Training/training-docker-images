<template>
    <div>
      <a class="hiddenanchor" id="signup"></a>
      <a class="hiddenanchor" id="signin"></a>

      <div class="login_wrapper">
        <div class="animate form login_form">
          <section class="login_content">
            <form>
              <h1>Register</h1>
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
              <div class="form-group">
                <label for="role">Role</label>
                <select v-model="role" class="form-control" id="role" disabled>
                  <option>admin</option>
                  <option>user</option>
                </select>
                </div>
              <input type="submit" class="btn btn-success" @click.prevent="Login" value="Create an account"/>
              <hr>
              <p>Already have an account ?
                <router-link to="login" class="btn btn-primary">Login</router-link>
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
        login: undefined,
        password: undefined,
        error: undefined,
        success: undefined,
        role: "user"
      }
    },
    methods: {
        Login(){
            if(this.login && this.password){
                var that = this;
                axios.post("/api/v1/auth/register",
                {
                    login: that.login,
                    password: that.password,
                    role: that.role
                },{withCredentials: true}).then(
                response => {
                    that.error = undefined;
                    that.success = undefined;
                    if(response.data.status=="error"){
                        that.error = response.data.message;
                    }
                    else if(response.data.status=="success"){
                        that.success = response.data.message;
                    }
                });
        }
      }
    }
}
</script>
