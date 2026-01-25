"use client";

import React, { useState, useEffect } from 'react';
import { api, endpoints, IMG_BASE_URL } from '../lib/api';
import { IncidentReport } from '../types';
import { RefreshCw, LayoutDashboard, CheckSquare, AlertCircle, CheckCircle2, List, Send, Map as MapIcon, ChevronRight, Activity, Database, ShieldCheck, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const AdminView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'verification'>('dashboard');
  const [incidents, setIncidents] = useState<IncidentReport[]>([]);
  const [loading, setLoading] = useState(false);
  const [assignForm, setAssignForm] = useState({ incidentId: '', workerId: 'worker_01' });
  const [MapComponent, setMapComponent] = useState<React.ComponentType<any> | null>(null);

  useEffect(() => {
    let isMounted = true;
    import('../components/IncidentMap')
      .then((mod) => {
        if (isMounted) {
          setMapComponent(() => mod.default);
        }
      })
      .catch((err) => {
        console.error("Critical: Map loading failed", err);
      });
    return () => { isMounted = false; };
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await api.get(endpoints.admin.reports);
      setIncidents(res.data);
    } catch (err) {
      console.error("Failed to fetch reports", err);
    } finally {
      setTimeout(() => setLoading(false), 800);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAssign = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assignForm.incidentId) return;
    const incident = incidents.find(i => i.id === Number(assignForm.incidentId));
    if (!incident) return;
    try {
      await api.post(endpoints.workflow.assign, {
        id: incident.id,
        type: incident.type,
        worker_id: assignForm.workerId
      });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleVerify = async (id: number, type: string, decision: 'approve' | 'reject') => {
    try {
      await api.post(endpoints.workflow.verify, { id, type, decision });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const pendingCount = incidents.filter(i => i.status === 'pending').length;
  const resolvedCount = incidents.filter(i => i.status === 'verified').length;
  const verificationQueue = incidents.filter(i => i.status === 'completed');

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { staggerChildren: 0.1 } }
  };

  return (
    <motion.div 
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="space-y-12"
    >
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-8">
        <div>
          <h1 className="text-5xl font-black text-stone-50 tracking-tighter">Command Center</h1>
          <p className="text-stone-400 text-lg font-medium mt-2">Bhopal infrastructure state & dispatch controller</p>
        </div>
        <div className="flex items-center gap-4">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={fetchData}
            disabled={loading}
            className="flex items-center gap-3 px-8 py-4 glass-warm border border-stone-700/50 rounded-2xl shadow-xl hover:bg-stone-800 transition-all font-black text-[10px] uppercase tracking-widest text-stone-100 disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-amber-500' : ''}`} />
            Refresh Nodes
          </motion.button>
        </div>
      </div>

      <div className="flex glass-warm p-2 rounded-[2rem] w-fit border border-stone-800/50">
        <button
          onClick={() => setActiveTab('dashboard')}
          className={`flex items-center gap-3 px-10 py-4 rounded-2xl font-black text-[10px] uppercase tracking-[0.2em] transition-all duration-500 ${activeTab === 'dashboard' ? 'bg-amber-600 text-white shadow-xl shadow-amber-900/40' : 'text-stone-500 hover:text-stone-300'}`}
        >
          <LayoutDashboard className="w-5 h-5" />
          Analytics & Dispatch
        </button>
        <button
          onClick={() => setActiveTab('verification')}
          className={`flex items-center gap-3 px-10 py-4 rounded-2xl font-black text-[10px] uppercase tracking-[0.2em] transition-all duration-500 relative ${activeTab === 'verification' ? 'bg-amber-600 text-white shadow-xl shadow-amber-900/40' : 'text-stone-500 hover:text-stone-300'}`}
        >
          <CheckSquare className="w-5 h-5" />
          Verification Gate
          {verificationQueue.length > 0 && (
            <span className="absolute -top-2 -right-2 flex h-6 w-6">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-6 w-6 bg-orange-500 text-[10px] font-black text-white items-center justify-center border-2 border-[#0c0a09]">
                {verificationQueue.length}
              </span>
            </span>
          )}
        </button>
      </div>

      <AnimatePresence mode="wait">
        {activeTab === 'dashboard' ? (
          <motion.div 
            key="dashboard"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="grid grid-cols-1 lg:grid-cols-4 gap-8"
          >
            <div className="lg:col-span-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
              {[
                { label: 'Active Alerts', val: pendingCount, icon: AlertCircle, color: 'text-orange-500', bg: 'bg-orange-500/10' },
                { label: 'Resolved Assets', val: resolvedCount, icon: CheckCircle2, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
                { label: 'Total Lifecycle', val: incidents.length, icon: Database, color: 'text-amber-500', bg: 'bg-amber-500/10' },
                { label: 'Node Health', val: '98.4%', icon: Activity, color: 'text-white', bg: 'bg-amber-600', dark: true }
              ].map((stat, i) => (
                <motion.div 
                  key={i}
                  whileHover={{ y: -5 }}
                  className={`glass-card p-8 rounded-[2.5rem] border border-stone-800 shadow-xl flex flex-col justify-between h-52 ${stat.dark ? 'bg-amber-600 !border-amber-500/50' : ''}`}
                >
                  <div className="flex items-center justify-between">
                    <div className={`p-4 ${stat.bg} ${stat.color} rounded-2xl border ${!stat.dark ? 'border-white/5' : 'border-white/20'}`}>
                      <stat.icon className="w-8 h-8" />
                    </div>
                    {!stat.dark && <ChevronRight className="w-5 h-5 text-stone-700" />}
                  </div>
                  <div>
                    <p className={`text-4xl font-black tracking-tighter ${stat.dark ? 'text-white' : 'text-stone-50'}`}>{stat.val}</p>
                    <p className={`text-[10px] font-black uppercase tracking-[0.3em] mt-1 ${stat.dark ? 'text-amber-100' : 'text-stone-500'}`}>{stat.label}</p>
                  </div>
                </motion.div>
              ))}
            </div>

            <div className="lg:col-span-3 space-y-8">
              <motion.div 
                className="glass-warm p-4 rounded-[3.5rem] shadow-2xl border border-stone-800 h-[600px] relative overflow-hidden"
              >
                <div className="absolute top-8 left-8 z-[10] glass-light px-6 py-3 rounded-2xl border border-white/5 shadow-xl flex items-center gap-3">
                  <MapIcon className="w-5 h-5 text-amber-500" />
                  <span className="text-[10px] font-black uppercase tracking-widest text-stone-100">Spatial Telemetry Overlay</span>
                </div>
                {MapComponent ? (
                  <MapComponent incidents={incidents} />
                ) : (
                  <div className="w-full h-full bg-stone-900/40 flex items-center justify-center">
                    <p className="text-stone-600 font-black uppercase tracking-[0.5em] text-[10px] animate-pulse">Initializing Map Engine...</p>
                  </div>
                )}
              </motion.div>

              <div className="glass-warm rounded-[3rem] border border-stone-800 shadow-xl overflow-hidden">
                 <div className="p-10 border-b border-stone-800/50 flex items-center justify-between bg-white/5">
                    <h3 className="text-2xl font-black text-stone-50 tracking-tighter">Real-time Feed</h3>
                    <button className="text-amber-500 text-[10px] font-black uppercase tracking-widest hover:text-amber-400 transition-colors">Export Ledger</button>
                 </div>
                 <div className="overflow-x-auto p-4">
                   <table className="w-full text-left border-separate border-spacing-y-2">
                     <thead>
                       <tr className="text-[10px] font-black text-stone-600 uppercase tracking-[0.3em]">
                         <th className="px-8 py-4">Incident</th>
                         <th className="px-8 py-4">Classification</th>
                         <th className="px-8 py-4">Status</th>
                         <th className="px-8 py-4">Personnel</th>
                       </tr>
                     </thead>
                     <tbody>
                       {incidents.slice(0, 8).map((i) => (
                         <tr key={i.id} className="group hover:bg-white/5 transition-colors cursor-default">
                           <td className="px-8 py-6 glass-warm rounded-l-2xl border-r-0 border-stone-800">
                             <p className="font-black text-amber-500 tracking-tight text-lg">#{i.id}</p>
                             <p className="text-[10px] text-stone-500 font-bold uppercase truncate max-w-[150px]">{i.location.address}</p>
                           </td>
                           <td className="px-8 py-6 glass-warm border-x-0 border-stone-800">
                             <span className="px-4 py-1.5 glass-light text-amber-200 text-[9px] font-black uppercase rounded-xl border border-white/5 tracking-widest">
                               {i.type}
                             </span>
                           </td>
                           <td className="px-8 py-6 glass-warm border-x-0 border-stone-800">
                             <div className="flex items-center gap-3">
                               <div className={`w-2 h-2 rounded-full ${i.status === 'pending' ? 'bg-orange-500' : i.status === 'completed' ? 'bg-amber-400' : 'bg-emerald-500'} animate-pulse`}></div>
                               <span className="text-[10px] font-black text-stone-200 uppercase tracking-widest">{i.status}</span>
                             </div>
                           </td>
                           <td className="px-8 py-6 glass-warm rounded-r-2xl border-l-0 border-stone-800 text-[10px] font-black text-stone-500 italic tracking-wider">
                             {i.assigned_to || 'WAITING'}
                           </td>
                         </tr>
                       ))}
                     </tbody>
                   </table>
                 </div>
              </div>
            </div>

            <div className="lg:col-span-1">
              <motion.div 
                whileHover={{ scale: 1.02 }}
                className="glass-card p-10 rounded-[3.5rem] shadow-2xl border border-stone-800 sticky top-24"
              >
                <div className="p-5 bg-amber-600 rounded-[1.5rem] w-fit mb-8 shadow-xl shadow-amber-900/40">
                  <Send className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-3xl font-black mb-2 tracking-tighter text-stone-50">Rapid Dispatch</h3>
                <p className="text-stone-500 text-sm font-medium mb-10 leading-relaxed">Direct personnel coordination for active Bhopal alerts.</p>
                
                <form onSubmit={handleAssign} className="space-y-8">
                  <div className="space-y-3">
                    <label className="text-[10px] font-black text-stone-600 uppercase tracking-[0.4em] ml-2">Target Alert</label>
                    <select
                      value={assignForm.incidentId}
                      onChange={(e) => setAssignForm({ ...assignForm, incidentId: e.target.value })}
                      className="w-full p-5 bg-stone-900/40 border border-stone-800 rounded-2xl outline-none focus:ring-2 focus:ring-amber-500/50 text-sm font-black text-stone-100 transition-all cursor-pointer"
                      required
                    >
                      <option value="">Select ID...</option>
                      {incidents.filter(i => i.status === 'pending').map(i => (
                        <option key={i.id} value={i.id}>#{i.id} - {i.type}</option>
                      ))}
                    </select>
                  </div>
                  
                  <div className="space-y-3">
                    <label className="text-[10px] font-black text-stone-600 uppercase tracking-[0.4em] ml-2">Field Operator</label>
                    <input
                      type="text"
                      value={assignForm.workerId}
                      onChange={(e) => setAssignForm({ ...assignForm, workerId: e.target.value })}
                      className="w-full p-5 bg-stone-900/40 border border-stone-800 rounded-2xl outline-none focus:ring-2 focus:ring-amber-500/50 text-sm font-black text-stone-100 transition-all placeholder-stone-700"
                      placeholder="Operator ID"
                      required
                    />
                  </div>

                  <button
                    type="submit"
                    className="w-full py-6 bg-amber-600 text-white font-black rounded-3xl hover:bg-amber-500 transition-all shadow-2xl shadow-amber-900/40 flex items-center justify-center gap-3 group uppercase text-[10px] tracking-widest"
                  >
                    Deploy Operator
                    <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </button>
                </form>
              </motion.div>
            </div>
          </motion.div>
        ) : (
          <motion.div 
            key="verification"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10"
          >
            {verificationQueue.length === 0 ? (
              <div className="md:col-span-full py-32 text-center glass-warm rounded-[4rem] border border-stone-800/50 flex flex-col items-center justify-center space-y-8 amber-glow">
                <div className="w-24 h-24 glass rounded-[2rem] flex items-center justify-center text-stone-700">
                  <ShieldCheck className="w-12 h-12" />
                </div>
                <div>
                  <p className="text-stone-50 font-black text-3xl tracking-tighter">Integrity Verified</p>
                  <p className="text-stone-500 font-medium text-lg mt-2">All field tasks have been human-audited or are clear.</p>
                </div>
              </div>
            ) : (
              verificationQueue.map((t) => (
                <motion.div 
                  key={t.id} 
                  whileHover={{ y: -10 }}
                  className="glass-card p-10 rounded-[3.5rem] border border-stone-800 shadow-2xl flex flex-col h-full relative overflow-hidden group"
                >
                  <div className="flex items-center justify-between mb-8 relative z-10">
                    <div>
                      <h4 className="font-black text-stone-50 text-2xl tracking-tighter">Fix Review #{t.id}</h4>
                      <p className="text-[10px] font-black text-stone-500 uppercase tracking-[0.3em] mt-1 truncate max-w-[150px]">{t.location.address}</p>
                    </div>
                    <span className="px-4 py-2 bg-emerald-500/10 text-emerald-400 text-[10px] font-black uppercase rounded-xl border border-emerald-500/20 tracking-widest">
                      {t.type}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-6 mb-10 flex-1 relative z-10">
                    <div className="space-y-4">
                      <p className="text-[10px] font-black text-stone-600 uppercase tracking-[0.4em] text-center">Reference</p>
                      <div className="aspect-[3/4] glass rounded-3xl overflow-hidden border border-white/5 relative group/img">
                        <img src={`${IMG_BASE_URL}/${t.images.original}`} alt="Original" className="w-full h-full object-cover grayscale opacity-40 group-hover/img:grayscale-0 group-hover/img:opacity-100 transition-all duration-700" />
                      </div>
                    </div>
                    <div className="space-y-4">
                      <p className="text-[10px] font-black text-stone-600 uppercase tracking-[0.4em] text-center">Field Proof</p>
                      <div className="aspect-[3/4] glass rounded-3xl overflow-hidden border border-amber-500/30 relative group/img">
                        <img src={`${IMG_BASE_URL}/${t.images.resolved}`} alt="Resolved" className="w-full h-full object-cover group-hover/img:scale-110 transition-transform duration-700" />
                        <div className="absolute inset-0 bg-amber-900/10 mix-blend-overlay"></div>
                      </div>
                    </div>
                  </div>

                  <div className="flex gap-4 relative z-10">
                    <button
                      onClick={() => handleVerify(t.id, t.type, 'approve')}
                      className="flex-1 py-5 bg-amber-600 text-white font-black rounded-2xl hover:bg-amber-500 transition-all shadow-xl shadow-amber-900/40 uppercase text-[10px] tracking-widest"
                    >
                      Audit Approve
                    </button>
                    <button
                      onClick={() => handleVerify(t.id, t.type, 'reject')}
                      className="w-16 h-16 glass rounded-2xl flex items-center justify-center text-stone-500 hover:text-red-400 hover:bg-red-400/5 transition-all border border-stone-800"
                    >
                      <X className="w-6 h-6" />
                    </button>
                  </div>
                </motion.div>
              ))
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default AdminView;