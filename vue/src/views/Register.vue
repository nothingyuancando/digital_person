<template>
    <div class="welcome-section">
      <h1>教育对话评估系统</h1>
      <p class="subtitle">基于人工智能的学生对话评估与分析平台</p>
    </div>
    <div class="register-container">
      <div class="image-section">
        <img src="@/assets/数据结构.jpg" alt="Register Image" />
      </div>
      <div class="form-section">
        <h1 class="section-title">注册</h1>
        <form>
          <div class="form-group">
            <label>用户名：</label>
            <input type="text" v-model="username" class="input-field" />
          </div>
          <div class="form-group">
            <label>密码：</label>
            <input type="password" v-model="password" class="input-field" />
          </div>
          <div class="form-group">
            <label>确认密码：</label>
            <input type="password" v-model="confirmPassword" class="input-field" />
          </div>
          <div class="form-group">
            <label>验证码：</label>
            <input type="text" v-model="verificationCode" class="input-field" />
            <span class="verification-code" @click="refreshCode">{{ verificationCodeText }}</span>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn">注册</button>
            <button type="button" class="btn btn-secondary">取消</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        confirmPassword: '',
        verificationCode: '',
        verificationCodeText: this.generateVerificationCode()
      };
    },
    methods: {
      generateVerificationCode() {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let code = '';
        for (let i = 0; i < 4; i++) {
          code += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return code;
      },
      refreshCode() {
        this.verificationCodeText = this.generateVerificationCode();
      }
    }
  };
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    max-width: 1000px;
    margin: 30px auto;
    background-color: #fff;
    border: 1px solid #eee;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  .welcome-section {
  margin-bottom: 30px;
  text-align: center;
}

.welcome-section h1 {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
  color: #606c7c;
}
  
  .image-section {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f9f9f9;
  }
  
  .image-section img {
    max-width: 100%;
    height: auto;
  }
  
  .form-section {
    flex: 1;
    padding: 30px;
  }
  
  .section-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #2c3e50;
    border-bottom: 2px solid #42b983;
    padding-bottom: 10px;
  }
  
  .form-group {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
  }
  
  .form-group label {
    width: 100px;
    font-weight: bold;
    text-align: right;
    margin-right: 10px;
  }
  
  .input-field {
    flex: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
  }
  
  .verification-code {
    margin-left: 10px;
    padding: 8px;
    background-color: #f0f0f0;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }
  
  .btn {
    display: inline-block;
    background: #42b983;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.3s;
    text-align: center;
    width: 120px;
  }
  
  .btn:hover {
    background: #3aa876;
  }
  
  .btn-secondary {
    background: #ccc;
    color: #333;
  }
  
  .btn-secondary:hover {
    background: #999;
  }
  </style>