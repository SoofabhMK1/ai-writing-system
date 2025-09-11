import { createRouter, createWebHistory } from 'vue-router';
import ProjectListView from '../views/ProjectListView.vue';
import ProjectDetailView from '../views/ProjectDetailView.vue';
import SettingsView from '../views/SettingsView.vue';
import ConversationView from '../views/ConversationView.vue';
import CharacterLibraryView from '../views/CharacterLibraryView.vue';

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
        path: '/projects/:projectId/conversation/:conversationId?',
        name: 'Conversation',
        component: ConversationView,
        props: true
    },
    {
      path: '/settings',
      name: 'Settings',
      component: SettingsView
    },
    {
      path: '/characters',
      name: 'CharacterLibrary',
      component: CharacterLibraryView
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
