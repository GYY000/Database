<template>
  <div class="container">
    <el-row>
      <el-col :span="1"></el-col>
      <el-col :span="12">
        <el-card class="vertical">
          <!-- 左边的竖直排列的卡片内容 -->
          <template #header>
            <div class="card-header">
              <h1>欢迎使用WGZForce！</h1>
            </div>
          </template>
          <img src="@/assets/image/welcome.jpg" style="width: 100%;"/>
        </el-card>
      </el-col>
      <el-col :span="1"></el-col>
      <el-col :span="8">
        <div class="horizontal-card-container">
          <el-card class="horizontal-card" style="height: 230px;">
            <!-- 右边上方的水平排列的卡片内容 -->
          </el-card>
          <el-card class="horizontal-card">
            <!-- 右边下方的水平排列的卡片内容 -->
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "main_page",
  setup() {

  }
}
</script>

<style scoped>
.container {
  margin: 20px;
}

.vertical-card {
  height: 300px;
}

.card-header {
  display: flex;
  justify-content: center;
  align-items: center;
}

.horizontal-card-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.horizontal-card {
  margin-bottom: 10px;
}
</style>