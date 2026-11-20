import axios from 'axios';
export const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://127.0.0.1:8000/api'});
export const mediaUrl=(path)=>{if(!path)return '';if(path.startsWith('http'))return path;return `${api.defaults.baseURL.replace(/\/api\/?$/,'')}${path.startsWith('/')?'':'/'}${path}`};
api.interceptors.request.use(config=>{const token=localStorage.getItem('access');if(token)config.headers.Authorization=`Bearer ${token}`;return config});
let refreshing=null;
api.interceptors.response.use(r=>r,async error=>{const original=error.config;if(error.response?.status===401&&!original?._retry&&localStorage.getItem('refresh')&&!original?.url?.includes('/auth/refresh/')){original._retry=true;try{refreshing??=axios.post(`${api.defaults.baseURL}/auth/refresh/`,{refresh:localStorage.getItem('refresh')}).finally(()=>refreshing=null);const r=await refreshing;localStorage.setItem('access',r.data.access);original.headers.Authorization=`Bearer ${r.data.access}`;return api(original)}catch{localStorage.removeItem('access');localStorage.removeItem('refresh');window.dispatchEvent(new Event('auth-expired'))}}return Promise.reject(error)});
export const items=(data)=>data?.results??(Array.isArray(data)?data:[]);
export const errText=(error)=>{const data=error.response?.data;if(typeof data==='string')return data;if(data?.detail)return data.detail;if(data&&typeof data==='object')return Object.entries(data).map(([k,v])=>`${k}: ${Array.isArray(v)?v.join(', '):v}`).join(' • ');return error.message||'Something went wrong'};
