<template>
  <div class="container">
    <div class="row">
      <div class="col-6 offset-sm-3 text-center">
        <form class="was-invalidated">
          <span class="alert">{{error}}</span>
          <div class="form-group">
            <label for="exampleInputEmail1">Email address</label>
            <input
              type="email"
              class="form-control"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
              placeholder="Enter email"
              v-model="email"
            >
            <small
              id="emailHelp"
              class="form-text text-muted"
            >We'll never share your email with anyone else.</small>
          </div>
          <div class="form-group">
            <label for="exampleInputPassword1">Password</label>
            <input
              type="password"
              class="form-control"
              id="exampleInputPassword1"
              placeholder="Password"
              v-model="password"
            >
          </div>
          <button type="submit" class="btn btn-primary" @click="loginSubmit">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "login",
  data() {
    return {
      email: "admin@example.com",
      password: "password",
      error: ''
    };
  },
  methods: {
    loginSubmit(e) {
      e.preventDefault();
      let data = { email: this.email, password: this.password };
      axios.post("/api/v1.0/user/auth", data).then(rqst => {
        localStorage.setItem("token", rqst.data.data.access_token);

        this.$router.push({name: 'chat'})
      }).catch(({response}) => {         
        
        switch (response.status) {
          case 401:            
            this.error = response.data.data
            break;        
          default:
            break;
        }       
        
      })
    }
  }
};
</script>
