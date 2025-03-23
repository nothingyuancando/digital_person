<template>
  <div class="history-list">
    <h1 class="section-title">历史对话记录</h1>
    
    <div class="search-container card">
      <div class="search-form">
        <input 
          type="text" 
          class="input-field" 
          placeholder="搜索对话内容、知识点或日期..." 
          v-model="searchQuery"
          @keyup.enter="searchHistory"
        >
        <div class="date-filters">
          <div class="date-filter">
            <label>开始日期</label>
            <input type="date" class="input-field" v-model="startDate">
          </div>
          <div class="date-filter">
            <label>结束日期</label>
            <input type="date" class="input-field" v-model="endDate">
          </div>
        </div>
        <button class="btn" @click="searchHistory">搜索</button>
        <button class="btn btn-secondary" @click="resetFilters">重置</button>
      </div>
    </div>
    
    <div class="card">
      <div v-if="loading" class="loading">
        <p>加载中...</p>
      </div>
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button class="btn" @click="fetchHistoryList">重试</button>
      </div>
      <div v-else-if="filteredHistory.length === 0" class="no-records">
        <p>没有找到符合条件的对话记录</p>
      </div>
      <div v-else class="history-content">
        <div class="history-table">
          <div class="table-header">
            <div class="column date-column">日期</div>
            <div class="column topic-column">主题</div>
            <div class="column score-column">分数</div>
            <div class="column actions-column">操作</div>
          </div>
          
          <div 
            v-for="(record, index) in paginatedHistory" 
            :key="record.id" 
            class="table-row"
            :class="{ 'row-alternate': index % 2 === 1 }"
          >
            <div class="column date-column">{{ record.date }}</div>
            <div class="column topic-column">{{ record.topic }}</div>
            <div class="column score-column">
              <span class="score-badge" :class="getScoreClass(record.score)">
                {{ record.score }}
              </span>
            </div>
            <div class="column actions-column">
              <button class="btn-small" @click="viewConversation(record.id)">查看对话</button>
              <button class="btn-small btn-secondary" @click="viewReport(record.id)">查看报告</button>
            </div>
          </div>
        </div>
        
        <div class="pagination">
          <button 
            class="pagination-btn" 
            :disabled="currentPage === 1"
            @click="currentPage--"
          >
            上一页
          </button>
          
          <div class="page-numbers">
            <button 
              v-for="page in displayedPages" 
              :key="page" 
              class="page-number"
              :class="{ active: currentPage === page }"
              @click="currentPage = page"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            class="pagination-btn" 
            :disabled="currentPage === totalPages"
            @click="currentPage++"
          >
            下一页
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HistoryList',
  data() {
    return {
      historyRecords: [],
      loading: true,
      error: null,
      searchQuery: '',
      startDate: '',
      endDate: '',
      currentPage: 1,
      pageSize: 10
    }
  },
  computed: {
    filteredHistory() {
      if (!this.searchQuery && !this.startDate && !this.endDate) {
        return this.historyRecords;
      }
      
      return this.historyRecords.filter(record => {
        let matchesSearch = true;
        let matchesDateRange = true;
        
        // 搜索过滤
        if (this.searchQuery) {
          const query = this.searchQuery.toLowerCase();
          matchesSearch = record.topic.toLowerCase().includes(query) || 
                          record.keywords.some(keyword => keyword.toLowerCase().includes(query));
        }
        
        // 日期范围过滤
        if (this.startDate) {
          const recordDate = new Date(record.date);
          const start = new Date(this.startDate);
          matchesDateRange = recordDate >= start;
        }
        
        if (this.endDate) {
          const recordDate = new Date(record.date);
          const end = new Date(this.endDate);
          end.setHours(23, 59, 59); // 设置为当天结束时间
          matchesDateRange = matchesDateRange && recordDate <= end;
        }
        
        return matchesSearch && matchesDateRange;
      });
    },
    paginatedHistory() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredHistory.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredHistory.length / this.pageSize);
    },
    displayedPages() {
      const pages = [];
      const maxPagesToShow = 5;
      
      if (this.totalPages <= maxPagesToShow) {
        // 如果总页数不多，显示所有页码
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i);
        }
      } else {
        // 否则显示当前页附近的页码
        let startPage = Math.max(1, this.currentPage - Math.floor(maxPagesToShow / 2));
        let endPage = startPage + maxPagesToShow - 1;
        
        if (endPage > this.totalPages) {
          endPage = this.totalPages;
          startPage = Math.max(1, endPage - maxPagesToShow + 1);
        }
        
        for (let i = startPage; i <= endPage; i++) {
          pages.push(i);
        }
      }
      
      return pages;
    }
  },
  created() {
    this.fetchHistoryList();
  },
  methods: {
    fetchHistoryList() {
      this.loading = true;
      this.error = null;
      
      // 这里应该调用实际的API接口获取历史记录列表
      // /api/history/conversations接口
      
      // 使用接口文档中的示例数据
      setTimeout(() => {
        try {
          // 使用API响应示例中的数据
          const apiResponse = {
            "status": "success",
            "data": {
              "totalRecords": 25,
              "records": [
                {
                  "recordId": "rec001",
                  "conversationTime": "2025-02-28T14:00:00Z",
                  "courseName": "数据结构",
                  "keyword": "二叉树基本概念"
                },
                {
                  "recordId": "rec002",
                  "conversationTime": "2025-02-27T15:30:00Z",
                  "courseName": "数据结构",
                  "keyword": "二叉树遍历方式"
                }
              ]
            }
          };
          
          // 基于API响应中的数据生成模拟数据，扩展为30条以保持界面效果
          const baseRecords = apiResponse.data.records;
          this.historyRecords = Array.from({ length: 30 }, (_, i) => {
            const baseIndex = i % baseRecords.length;
            const baseRecord = baseRecords[baseIndex];
            
            // 创建日期递减效果
            const date = new Date(baseRecord.conversationTime);
            date.setDate(date.getDate() - i);
            const formattedDate = date.toISOString().split('T')[0];
            
            // 生成随机分数
            const randomScore = Math.floor(Math.random() * 41) + 60; // 60-100分
            
            return {
              id: baseRecord.recordId + '-' + i,
              date: formattedDate,
              topic: `${baseRecord.courseName} - ${baseRecord.keyword}`,
              score: randomScore,
              keywords: [baseRecord.keyword, baseRecord.courseName, '对话', '学习']
            };
          });
          
          this.loading = false;
        } catch (err) {
          this.error = '获取历史记录失败，请重试';
          this.loading = false;
        }
      }, 1000);
    },
    searchHistory() {
      this.currentPage = 1; // 重置到第一页
      // 搜索已在计算属性中处理
    },
    resetFilters() {
      this.searchQuery = '';
      this.startDate = '';
      this.endDate = '';
      this.currentPage = 1;
    },
    getScoreClass(score) {
      if (score >= 90) return 'score-a';
      if (score >= 80) return 'score-b';
      if (score >= 70) return 'score-c';
      if (score >= 60) return 'score-d';
      return 'score-f';
    },
    viewConversation(id) {
      // 跳转到历史对话详情页
      this.$router.push(`/history-detail/${id}?tab=conversation`);
    },
    viewReport(id) {
      // 跳转到历史分析报告页
      this.$router.push(`/history-detail/${id}?tab=report`);
    }
  }
}
</script>

<style scoped>
.history-list {
  max-width: 1000px;
  margin: 0 auto;
}

.search-container {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-end;
}

.search-form .input-field {
  flex: 1;
  min-width: 250px;
}

.date-filters {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.date-filter {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.date-filter label {
  font-size: 14px;
  margin-bottom: 5px;
  color: #606c7c;
}

.date-filter .input-field {
  width: 150px;
}

.history-content {
  display: flex;
  flex-direction: column;
}

.history-table {
  width: 100%;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  display: flex;
  background-color: #f8f8f8;
  font-weight: bold;
  border-bottom: 2px solid #eee;
}

.table-row {
  display: flex;
  border-bottom: 1px solid #eee;
}

.row-alternate {
  background-color: #f9f9f9;
}

.column {
  padding: 15px;
  text-align: left;
  display: flex;
  align-items: center;
}

.date-column {
  width: 120px;
}

.topic-column {
  flex: 1;
}

.score-column {
  width: 80px;
  justify-content: center;
}

.actions-column {
  width: 200px;
  justify-content: flex-end;
  gap: 10px;
}

.score-badge {
  display: inline-block;
  min-width: 36px;
  padding: 2px 8px;
  border-radius: 12px;
  text-align: center;
  font-weight: bold;
}

.score-a {
  background-color: #e1f3d8;
  color: #52c41a;
}

.score-b {
  background-color: #e6f7ff;
  color: #1890ff;
}

.score-c {
  background-color: #fff7e6;
  color: #fa8c16;
}

.score-d {
  background-color: #f0f0f0;
  color: #606c7c;
}

.score-f {
  background-color: #fff1f0;
  color: #f5222d;
}

.btn-small {
  padding: 6px 12px;
  font-size: 12px;
  border-radius: 4px;
  cursor: pointer;
  background: #42b983;
  color: white;
  border: none;
  transition: background 0.3s;
}

.btn-small:hover {
  background: #3aa876;
}

.btn-small.btn-secondary {
  background: #606c7c;
}

.btn-small.btn-secondary:hover {
  background: #4e5a69;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.pagination-btn {
  padding: 8px 15px;
  border: 1px solid #d9d9d9;
  background: white;
  color: #606c7c;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  color: #42b983;
  border-color: #42b983;
}

.pagination-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.page-numbers {
  display: flex;
  gap: 5px;
}

.page-number {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #d9d9d9;
  background: white;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
}

.page-number:hover {
  color: #42b983;
  border-color: #42b983;
}

.page-number.active {
  background: #42b983;
  color: white;
  border-color: #42b983;
}

.no-records, .loading, .error {
  padding: 40px 20px;
  text-align: center;
}

.error {
  color: #f56c6c;
}
</style> 