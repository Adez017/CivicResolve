"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, ShieldCheck, MapPin, Trash2, AlertTriangle, 
  ArrowRight, CheckCircle2, Globe, Users, Loader2, 
  X, Database, LayoutList, BarChart3, Filter, Sparkles
} from 'lucide-react';
import { IncidentReport } from '../types';
import { api, endpoints } from '../lib/api';
import dynamic from 'next/dynamic';

const IncidentMap = dynamic(() => import('../components/IncidentMap'), { 
  ssr: false,
  loading: () => <div className="h-full w-full bg-stone-900/50 animate-pulse flex items-center justify-center text-stone-500 font-bold uppercase tracking-widest text-xs">Initializing Neural Map...</div>
});

interface LandingViewProps {
  onEnterPortal: () => void;
}

const LandingView: React.FC<LandingViewProps> = ({ onEnterPortal }) => {
  const [incidents, setIncidents] = useState<IncidentReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [showTable, setShowTable] = useState(false);
  const [stats, setStats] = useState({
    garbage: 0,
    potholes: 0,
    resolutionRate: "0",
    totalNodes: 0
  });

  useEffect(() => {
    const fetchPublicData = async () => {
      try {
        const res = await api.get<IncidentReport[]>(endpoints.admin.reports);
        const data = res.data;
        setIncidents(data);

        const garbageCount = data.filter(i => i.type.toLowerCase().includes('garbage')).length;
        const potholeCount = data.filter(i => i.type.toLowerCase().includes('pothole')).length;
        const resolved = data.filter(i => i.status === 'verified' || i.status === 'completed').length;
        const rate = data.length > 0 ? ((resolved / data.length) * 100).toFixed(1) : "0";

        setStats({
          garbage: garbageCount,
          potholes: potholeCount,
          resolutionRate: rate,
          totalNodes: data.length
        });
      } catch (err) {
        console.error("Failed to fetch database records:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchPublicData();
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { staggerChildren: 0.15, delayChildren: 0.3 }
    }
  };

  const itemVariants = {
    hidden: { y: 30, opacity: 0 },
    visible: { 
      y: 0, 
      opacity: 1, 
      transition: { type: 'spring', damping: 20, stiffness: 100 } 
    }
  };

  return (
    <div className="min-h-screen mesh-gradient-warm selection:bg-amber-500/30 overflow-x-hidden text-stone-100">
      {/* Background Orbs */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none z-0">
        <div className="absolute top-[5%] left-[10%] w-[500px] h-[500px] bg-amber-600/10 rounded-full blur-[120px] animate-pulse-slow"></div>
        <div className="absolute bottom-[10%] right-[5%] w-[600px] h-[600px] bg-orange-700/10 rounded-full blur-[150px] animate-pulse-slow" style={{ animationDelay: '3s' }}></div>
      </div>

      {/* Navigation */}
      <motion.nav 
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="fixed top-0 inset-x-0 h-20 glass-warm z-50 px-6 border-b border-stone-800/50"
      >
        <div className="max-w-7xl mx-auto h-full flex items-center justify-between">
          <motion.div 
            whileHover={{ scale: 1.02 }}
            className="flex items-center gap-3 cursor-pointer"
          >
            <div className="p-2.5 bg-amber-600 rounded-xl shadow-lg shadow-amber-900/30">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <span className="font-black text-2xl tracking-tighter text-stone-50">CivicResolve</span>
          </motion.div>
          
          <div className="flex items-center gap-8">
            <button 
              onClick={() => setShowTable(true)}
              className="hidden md:flex items-center gap-2 text-sm font-bold text-stone-400 hover:text-amber-200 transition-colors"
            >
              <LayoutList className="w-4 h-4" />
              Live Feed
            </button>
            <motion.button 
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onEnterPortal}
              className="px-6 py-2.5 bg-stone-100 text-stone-900 font-black rounded-xl shadow-xl hover:bg-amber-50 transition-all text-sm flex items-center gap-2"
            >
              Control Center
              <ArrowRight className="w-4 h-4" />
            </motion.button>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section className="relative pt-48 pb-32 px-6 z-10">
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="max-w-7xl mx-auto text-center"
        >
          <motion.div variants={itemVariants} className="inline-flex items-center gap-2 px-5 py-2 glass-light rounded-full text-amber-400 text-[10px] font-black uppercase tracking-[0.25em] mb-12 border border-amber-500/20">
            <Sparkles className="w-4 h-4" />
            Bhopal Smart Infrastructure Node
          </motion.div>
          
          <motion.h1 variants={itemVariants} className="text-7xl md:text-[10rem] font-black tracking-tighter leading-[0.8] mb-14 text-stone-50">
            HARMONIOUS<br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-orange-300 to-amber-500 text-warm-glow">URBAN FLOW</span>
          </motion.h1>

          <motion.p variants={itemVariants} className="max-w-2xl mx-auto text-stone-400 text-xl font-medium mb-16 leading-relaxed">
            A gentle yet powerful gaze over Bhopal. Our AI nodes identify infrastructure needs with precision, ensuring every street feels like home.
          </motion.p>

          <motion.div variants={itemVariants} className="flex flex-wrap justify-center gap-6">
            <motion.button 
              whileHover={{ scale: 1.05, boxShadow: '0 0 50px rgba(245, 158, 11, 0.3)' }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowTable(true)}
              className="px-12 py-6 bg-amber-600 text-white font-black rounded-3xl shadow-2xl flex items-center gap-3 transition-all group"
            >
              Explore Public Dataset
              <Database className="w-5 h-5 group-hover:rotate-12 transition-transform" />
            </motion.button>
            <div className="px-10 py-6 glass-warm rounded-3xl flex items-center gap-5 group border border-stone-700/50">
              <Users className="w-6 h-6 text-amber-400 group-hover:scale-110 transition-transform" />
              <div className="text-left">
                <p className="text-3xl font-black leading-none text-stone-50">{loading ? '...' : stats.totalNodes}</p>
                <p className="text-[10px] font-black text-stone-500 uppercase tracking-widest mt-1">Active Alerts</p>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </section>

      {/* Stats Bento Grid */}
      <section className="py-24 px-6 relative z-10">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="grid grid-cols-1 md:grid-cols-4 gap-8"
          >
            <motion.div 
              variants={itemVariants}
              className="md:col-span-2 p-10 glass-card rounded-[3rem] flex flex-col justify-between h-80 relative overflow-hidden"
            >
              <div className="flex justify-between items-start relative z-10">
                <div className="p-5 bg-amber-500/10 text-amber-500 rounded-2xl border border-amber-500/20">
                  <Trash2 className="w-8 h-8" />
                </div>
                <div className="px-3 py-1.5 glass-light text-amber-200 rounded-full border border-white/5 text-[9px] font-black tracking-widest uppercase">
                  Sanitation Focus
                </div>
              </div>
              <div className="relative z-10">
                <h3 className="text-7xl font-black tracking-tighter mb-2 text-stone-50">
                  {loading ? <Loader2 className="w-8 h-8 animate-spin inline" /> : stats.garbage}
                </h3>
                <p className="text-stone-500 font-bold uppercase text-xs tracking-[0.2em]">Garbage Reports in Database</p>
              </div>
            </motion.div>

            <motion.div 
              variants={itemVariants}
              className="p-10 glass-card rounded-[3rem] flex flex-col justify-between h-80 relative overflow-hidden"
            >
              <div className="p-5 bg-orange-500/10 text-orange-500 rounded-2xl border border-orange-500/20 w-fit">
                <AlertTriangle className="w-8 h-8" />
              </div>
              <div>
                <h3 className="text-7xl font-black tracking-tighter mb-2 text-stone-50">
                  {loading ? '...' : stats.potholes}
                </h3>
                <p className="text-stone-500 font-bold uppercase text-xs tracking-[0.2em]">Pothole Repairs</p>
              </div>
            </motion.div>

            <motion.div 
              variants={itemVariants}
              className="p-10 bg-amber-600 rounded-[3rem] flex flex-col justify-between h-80 shadow-2xl shadow-amber-900/40 relative group overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-amber-500 to-orange-600 opacity-50"></div>
              <div className="p-5 bg-white/20 rounded-2xl border border-white/20 w-fit relative z-10">
                <CheckCircle2 className="w-8 h-8 text-white" />
              </div>
              <div className="relative z-10">
                <h3 className="text-7xl font-black tracking-tighter mb-2 text-white">{loading ? '...' : stats.resolutionRate}%</h3>
                <p className="text-amber-100 font-bold uppercase text-xs tracking-[0.2em]">Resolution Score</p>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Interactive Map Section */}
      <section className="py-32 px-6 relative z-10">
        <div className="max-w-7xl mx-auto space-y-16">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-10">
            <motion.div 
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="space-y-4"
            >
              <h2 className="text-5xl md:text-6xl font-black tracking-tighter text-stone-50">Civic Cartography</h2>
              <p className="text-stone-400 text-lg max-w-xl font-medium">Visualizing every coordinate and report stored within the civicresolve.db. Centered on Bhopal Metro.</p>
            </motion.div>
            <div className="flex items-center gap-5 glass-warm px-8 py-5 rounded-3xl border border-stone-700/50">
              <div className="w-12 h-12 bg-amber-500/20 text-amber-500 rounded-2xl flex items-center justify-center border border-amber-500/20">
                <MapPin className="w-6 h-6" />
              </div>
              <div>
                <p className="text-[10px] font-black uppercase tracking-widest text-stone-500">Regional Focus</p>
                <p className="font-black text-stone-100 uppercase tracking-wider text-sm">Bhopal, MP, India</p>
              </div>
            </div>
          </div>

          <motion.div 
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass-warm p-4 rounded-[4rem] overflow-hidden h-[750px] relative border border-stone-800 shadow-2xl"
          >
            <div className="absolute top-12 right-12 z-10 glass-warm px-8 py-8 rounded-[2.5rem] border border-stone-700/50 space-y-6 shadow-2xl">
              <div className="flex items-center gap-4">
                <div className="w-5 h-5 rounded-full bg-amber-500 ring-4 ring-amber-500/10 shadow-lg shadow-amber-500/40"></div>
                <span className="text-[10px] font-black uppercase tracking-[0.3em] text-stone-300">Pending Fix</span>
              </div>
              <div className="flex items-center gap-4">
                <div className="w-5 h-5 rounded-full bg-orange-400 ring-4 ring-orange-400/10 shadow-lg shadow-orange-400/40"></div>
                <span className="text-[10px] font-black uppercase tracking-[0.3em] text-stone-300">Active Resolve</span>
              </div>
              <div className="pt-6 border-t border-stone-800">
                 <button 
                  onClick={() => setShowTable(true)}
                  className="w-full py-4 bg-stone-100 text-stone-900 hover:bg-amber-50 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all shadow-xl"
                 >
                   Open Master Table
                 </button>
              </div>
            </div>
            <IncidentMap incidents={incidents} center={[23.2599, 77.4126]} zoom={13} />
          </motion.div>
        </div>
      </section>

      {/* Dataset Summary Modal */}
      <AnimatePresence>
        {showTable && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] flex items-center justify-center p-6 md:p-12"
          >
            <div className="absolute inset-0 bg-[#0c0a09]/80 backdrop-blur-xl" onClick={() => setShowTable(false)}></div>
            <motion.div 
              initial={{ scale: 0.95, y: 40, opacity: 0 }}
              animate={{ scale: 1, y: 0, opacity: 1 }}
              exit={{ scale: 0.95, y: 40, opacity: 0 }}
              className="glass-warm w-full max-w-6xl h-full max-h-[85vh] rounded-[3.5rem] border border-stone-800 relative z-10 flex flex-col overflow-hidden shadow-2xl amber-glow"
            >
              {/* Modal Header */}
              <div className="p-12 border-b border-stone-800/50 flex items-center justify-between bg-stone-900/20">
                <div>
                  <div className="flex items-center gap-4 mb-3">
                    <div className="p-3 bg-amber-600/20 rounded-2xl border border-amber-600/30">
                      <Database className="w-8 h-8 text-amber-500" />
                    </div>
                    <h2 className="text-4xl font-black tracking-tighter text-stone-50">Infrastructure Ledger</h2>
                  </div>
                  <p className="text-stone-400 text-lg font-medium">Summarized view of Bhopal's live civic records.</p>
                </div>
                <button 
                  onClick={() => setShowTable(false)}
                  className="w-16 h-16 glass-warm rounded-3xl flex items-center justify-center hover:bg-stone-800 transition-colors border border-stone-700"
                >
                  <X className="w-8 h-8 text-stone-400" />
                </button>
              </div>

              {/* Data Table */}
              <div className="flex-1 overflow-y-auto p-12 hide-scrollbar bg-[#0c0a09]/40">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
                   <div className="p-8 glass-card rounded-3xl border border-stone-800">
                      <BarChart3 className="w-6 h-6 text-amber-500 mb-4" />
                      <p className="text-3xl font-black text-stone-50">{incidents.length}</p>
                      <p className="text-[10px] font-black text-stone-500 uppercase tracking-widest mt-1">Total Indexed Records</p>
                   </div>
                   <div className="p-8 glass-card rounded-3xl border border-stone-800">
                      <Filter className="w-6 h-6 text-orange-500 mb-4" />
                      <p className="text-3xl font-black text-stone-50">Bhopal Central</p>
                      <p className="text-[10px] font-black text-stone-500 uppercase tracking-widest mt-1">Active Monitoring Zone</p>
                   </div>
                </div>

                <table className="w-full text-left border-separate border-spacing-y-4">
                  <thead>
                    <tr className="text-[11px] font-black text-stone-600 uppercase tracking-[0.3em]">
                      <th className="px-8 pb-4">Identifier</th>
                      <th className="px-8 pb-4">Classification</th>
                      <th className="px-8 pb-4">Spatial Context</th>
                      <th className="px-8 pb-4">Current State</th>
                    </tr>
                  </thead>
                  <tbody>
                    {incidents.map((inc) => (
                      <tr key={inc.id} className="group cursor-default">
                        <td className="px-8 py-6 glass-warm rounded-l-[1.5rem] border-r-0 border-stone-800 text-amber-400 font-black">
                          #{inc.id.toString().padStart(4, '0')}
                        </td>
                        <td className="px-8 py-6 glass-warm border-x-0 border-stone-800">
                          <span className="text-sm font-black uppercase tracking-wider text-stone-200 group-hover:text-amber-200 transition-colors">
                            {inc.type}
                          </span>
                        </td>
                        <td className="px-8 py-6 glass-warm border-x-0 border-stone-800">
                          <div className="flex items-center gap-2 text-stone-500 group-hover:text-stone-300 transition-colors">
                            <MapPin className="w-3.5 h-3.5" />
                            <p className="text-xs font-bold truncate max-w-[250px]">{inc.location.address}</p>
                          </div>
                        </td>
                        <td className="px-8 py-6 glass-warm rounded-r-[1.5rem] border-l-0 border-stone-800">
                          <div className="flex items-center gap-3">
                            <div className={`w-2.5 h-2.5 rounded-full ${inc.status === 'verified' || inc.status === 'completed' ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.4)]' : 'bg-amber-500 animate-pulse'}`}></div>
                            <span className={`text-[10px] font-black uppercase tracking-widest ${inc.status === 'verified' || inc.status === 'completed' ? 'text-emerald-500' : 'text-amber-500'}`}>
                              {inc.status}
                            </span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              <div className="p-8 border-t border-stone-800/50 bg-stone-900/40 text-center">
                 <p className="text-[10px] font-black uppercase tracking-[0.5em] text-stone-600">Secure Spatial Ledger • Localhost Sync v4.20</p>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Footer */}
      <footer className="py-40 relative z-10 border-t border-stone-800/50 bg-[#0c0a09]/80">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-24">
            <div className="md:col-span-2 space-y-12">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-amber-600 rounded-2xl">
                  <Activity className="w-8 h-8 text-white" />
                </div>
                <span className="font-black text-4xl tracking-tighter text-stone-50">CivicResolve</span>
              </div>
              <p className="text-stone-400 text-xl font-medium leading-relaxed max-w-lg">
                Advancing the aesthetics and efficiency of urban life through neural vision. Bhopal's trusted infrastructure partner.
              </p>
              <div className="flex gap-10">
                 {['Twitter', 'Journal', 'Network'].map(s => (
                   <a key={s} href="#" className="text-xs font-black uppercase tracking-widest text-stone-600 hover:text-amber-400 transition-colors underline underline-offset-8">{s}</a>
                 ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-black uppercase tracking-[0.4em] text-[10px] text-stone-600 mb-10">Architecture</h4>
              <ul className="space-y-8 text-sm font-bold text-stone-500">
                <li><a href="#" className="hover:text-amber-400 transition-colors">Neural Mapping v4</a></li>
                <li><a href="#" className="hover:text-amber-400 transition-colors">YOLO Detection Engine</a></li>
                <li><a href="#" className="hover:text-amber-400 transition-colors">Worker API Mesh</a></li>
              </ul>
            </div>

            <div className="space-y-10">
              <h4 className="font-black uppercase tracking-[0.4em] text-[10px] text-stone-600 mb-10">System State</h4>
              <div className="p-10 glass-warm rounded-[2.5rem] border-stone-800 space-y-8">
                <div>
                  <p className="text-[10px] font-black text-stone-600 uppercase tracking-widest mb-2">Connected DB</p>
                  <p className="text-xs font-black text-amber-500 flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></div>
                    CIVICRESOLVE.DB ACTIVE
                  </p>
                </div>
                <div>
                  <p className="text-[10px] font-black text-stone-600 uppercase tracking-widest mb-2">Global Load</p>
                  <p className="text-xs font-black text-stone-200">OPTIMAL • 12ms Sync</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-40 pt-16 border-t border-stone-800/50 flex flex-col md:flex-row items-center justify-between gap-10 text-stone-600 text-[10px] font-black uppercase tracking-[0.6em]">
            <span>&copy; {new Date().getFullYear()} Bhopal Smart City Hub</span>
            <span className="text-amber-600/50">Eyes On Infrastructure</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingView;