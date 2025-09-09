import { createRouter, createWebHistory } from 'vue-router';
import ProjectListView from '../views/ProjectListView.vue';
import ProjectDetailView from '../views/ProjectDetailView.vue';
import SettingsView from '../views/SettingsView.vue';

const routes = [
    {
      path: '/',
      name: 'ProjectList',
      component: ProjectListView
    },
    {
      path: '/projects/:projectId',
      name: 'ProjectDetail',
      component: ProjectDetailView
    },
    {
      path: '/settings',
      name: 'Settings',
      component: SettingsView
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
