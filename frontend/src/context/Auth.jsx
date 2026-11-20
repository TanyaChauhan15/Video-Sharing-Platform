import React,{createContext,useContext,useEffect,useState} from 'react';import {api} from '../api';
const Context=createContext(null);export const useAuth=()=>useContext(Context);
export function AuthProvider({children}){const [user,setUser]=useState(null),[loading,setLoading]=useState(true);
const load=async()=>{if(!localStorage.getItem('access')){setUser(null);setLoading(false);return}try{setUser((await api.get('/auth/profile/')).data)}catch{setUser(null)}finally{setLoading(false)}};
useEffect(()=>{load();const clear=()=>{setUser(null)};window.addEventListener('auth-expired',clear);return()=>window.removeEventListener('auth-expired',clear)},[]);
const login=async(username,password)=>{const {data}=await api.post('/auth/login/',{username,password});localStorage.setItem('access',data.access);localStorage.setItem('refresh',data.refresh);await load()};
const logout=()=>{localStorage.removeItem('access');localStorage.removeItem('refresh');setUser(null)};
return <Context.Provider value={{user,loading,login,logout,load}}>{children}</Context.Provider>}
