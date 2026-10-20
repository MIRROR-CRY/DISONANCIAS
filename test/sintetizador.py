#!/usr/bin/env python3
import numpy as np
from scipy.io import wavfile
import os
import json
import time

class Sintetizador:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.tempo = 120
        self.canales = {}

    def nota_a_frecuencia(self, nota):
        return 440 * (2 ** ((nota - 69) / 12))

    def generar_onda(self, tipo, frecuencia, duracion, volumen=0.5):
        n_samples = int(self.sample_rate * duracion)
        t = np.linspace(0, duracion, n_samples)
        
        if tipo == "sine":
            onda = np.sin(2 * np.pi * frecuencia * t)
        elif tipo == "square":
            onda = np.sign(np.sin(2 * np.pi * frecuencia * t))
        elif tipo == "sawtooth":
            onda = 2 * (t * frecuencia - np.floor(t * frecuencia + 0.5))
        elif tipo == "triangle":
            onda = 2 * np.abs(2 * (t * frecuencia - np.floor(t * frecuencia + 0.5))) - 1
        elif tipo == "noise":
            onda = np.random.uniform(-1, 1, n_samples)
        else:
            onda = np.sin(2 * np.pi * frecuencia * t)
        
        return onda * volumen

    def envolvente(self, onda, attack=0.01, decay=0.1, sustain=0.7, release=0.2, duracion_total=None):
        n = len(onda)
        if duracion_total is None:
            duracion_total = n / self.sample_rate
        
        attack_samples = int(self.sample_rate * attack)
        decay_samples = int(self.sample_rate * decay)
        release_start = n - int(self.sample_rate * release)
        
        envolvente = np.ones(n)
        
        for i in range(attack_samples):
            envolvente[i] = i / attack_samples
        
        for i in range(decay_samples):
            idx = attack_samples + i
            if idx < n:
                envolvente[idx] = 1 - (1 - sustain) * (i / decay_samples)
        
        for i in range(release_start, n):
            envolvente[i] = sustain * (n - i) / (n - release_start)
        
        return onda * envolvente

    def agregar_instrumento(self, nombre, tipo_onda, attack=0.01, decay=0.1, sustain=0.7, release=0.2):
        self.canales[nombre] = {
            "tipo": tipo_onda,
            "attack": attack,
            "decay": decay,
            "sustain": sustain,
            "release": release
        }

    def tocar_nota(self, nota, duracion=1.0, instrumento="default", volumen=0.5):
        freq = self.nota_a_frecuencia(nota)
        
        if instrumento not in self.canales:
            instrumento = "default"
        
        config = self.canales.get(instrumento, {
            "tipo": "sine",
            "attack": 0.01,
            "decay": 0.1,
            "sustain": 0.7,
            "release": 0.2
        })
        
        onda = self.generar_onda(config["tipo"], freq, duracion, volumen)
        env_config = {k: v for k, v in config.items() if k != "tipo"}
        onda = self.envolvente(onda, **env_config)
        
        return onda

    def secuencia(self, notas, duracion_nota=0.5, instrumento="default", volumen=0.5):
        notas_array = notas.split()
        onda_total = np.array([])
        
        for nota in notas_array:
            nota = nota.strip()
            if not nota:
                continue
            
            if nota.startswith("-"):
                dur = float(nota[1:])
                silencio = np.zeros(int(self.sample_rate * dur))
                onda_total = np.concatenate([onda_total, silencio])
            elif nota.startswith("r"):
                octave = int(nota[1]) if len(nota) > 1 else 4
                nota_num = self._nota_a_num(nota[0], octave)
                onda = self.tocar_nota(nota_num, duracion_nota, instrumento, volumen)
                onda_total = np.concatenate([onda_total, onda])
            elif nota[0].isalpha():
                octave = 4
                if len(nota) > 1 and nota[-1].isdigit():
                    octave = int(nota[-1])
                    nota = nota[:-1]
                nota_num = self._nota_a_num(nota[0], octave)
                onda = self.tocar_nota(nota_num, duracion_nota, instrumento, volumen)
                onda_total = np.concatenate([onda_total, onda])
            else:
                nota_num = int(nota)
                onda = self.tocar_nota(nota_num, duracion_nota, instrumento, volumen)
                onda_total = np.concatenate([onda_total, onda])
        
        return onda_total

    def _nota_a_num(self, nota, octava):
        notas = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
        if "#" in nota:
            notas[nota[0]] += 1
        return 12 * (octava + 1) + notas.get(nota[0].lower(), 60)

    def crear_proyecto(self, nombre, bpm=120):
        self.tempo = bpm
        self.proyecto = {
            "nombre": nombre,
            "bpm": bpm,
            "tracks": []
        }

    def agregar_track(self, nombre, instrumento, volumen=0.8):
        self.proyecto["tracks"].append({
            "nombre": nombre,
            "instrumento": instrumento,
            "volumen": volumen,
            "notas": []
        })

    def agregar_nota_track(self, track_idx, nota, inicio, duracion):
        if track_idx < len(self.proyecto["tracks"]):
            self.proyecto["tracks"][track_idx]["notas"].append({
                "nota": nota,
                "inicio": inicio,
                "duracion": duracion
            })

    def renderizar(self, duracion_total):
        duracion_samples = int(self.sample_rate * duracion_total)
        mezcla = np.zeros(duracion_samples)
        
        for track in self.proyecto["tracks"]:
            base_config = self.canales.get(track["instrumento"], {"tipo": "sine", "attack": 0.01, "decay": 0.1, "sustain": 0.7, "release": 0.2})
            config = {k: v for k, v in base_config.items() if k != "tipo"}
            track_onda = np.zeros(duracion_samples)
            
            for nota in track["notas"]:
                freq = self.nota_a_frecuencia(nota["nota"])
                inicio = int(self.sample_rate * nota["inicio"])
                dur = nota["duracion"]
                
                onda = self.generar_onda(config["tipo"], freq, dur, 1.0)
                onda = self.envolvente(onda, **config)
                
                fin = min(inicio + len(onda), duracion_samples)
                if inicio < duracion_samples:
                    track_onda[inicio:fin] += onda[:fin-inicio]
            
            mezcla += track_onda * track["volumen"]
        
        max_val = np.max(np.abs(mezcla))
        if max_val > 0:
            mezcla = mezcla / max_val * 0.8
        
        return mezcla

    def guardar_wav(self, onda, filename):
        onda_int16 = (onda * 32767).astype(np.int16)
        wavfile.write(filename, self.sample_rate, onda_int16)
        print(f"Guardado: {filename}")

    def reproducir(self, filename):
        if os.name == "nt":
            os.system(f"start {filename}")
        elif os.name == "posix":
            if "WAYLAND_DISPLAY" in os.environ or "DISPLAY" in os.environ:
                os.system(f"xdg-open {filename} &")
            else:
                print(f"Abre manualmente: {filename}")

def ejemplo_basico():
    s = Sintetizador()
    s.agregar_instrumento("lead", "sawtooth", attack=0.05, decay=0.2, sustain=0.6, release=0.3)
    s.agregar_instrumento("bass", "square", attack=0.01, decay=0.3, sustain=0.4, release=0.2)
    s.agregar_instrumento("pad", "sine", attack=0.5, decay=0.3, sustain=0.8, release=0.5)
    
    onda = s.secuencia("c4 e4 g4 b4 c5", duracion_nota=0.4, instrumento="lead", volumen=0.7)
    onda2 = s.secuencia("c2 c2 f2 g2", duracion_nota=0.8, instrumento="bass", volumen=0.5)
    
    max_len = max(len(onda), len(onda2))
    onda = np.pad(onda, (0, max_len - len(onda)))
    onda2 = np.pad(onda2, (0, max_len - len(onda2)))
    mezcla = onda + onda2
    s.guardar_wav(mezcla, "musica/ejemplo.wav")
    s.reproducir("musica/ejemplo.wav")

def ejemplo_proyecto():
    s = Sintetizador()
    
    s.agregar_instrumento("kick", "sine")
    s.agregar_instrumento("snare", "noise")
    s.agregar_instrumento("bass", "sawtooth", attack=0.02, decay=0.2, sustain=0.5, release=0.2)
    s.agregar_instrumento("melodia", "square", attack=0.05, decay=0.1, sustain=0.6, release=0.2)
    s.agregar_instrumento("acordes", "triangle", attack=0.3, decay=0.2, sustain=0.5, release=0.4)
    
    s.crear_proyecto("mi_cancion", bpm=128)
    s.agregar_track("bateria", "kick", volumen=0.8)
    s.agregar_track("bajo", "bass", volumen=0.7)
    s.agregar_track("melodia", "melodia", volumen=0.6)
    s.agregar_track("acordes", "acordes", volumen=0.5)
    
    s.agregar_nota_track(0, 36, 0.0, 0.5)
    s.agregar_nota_track(0, 38, 1.0, 0.25)
    s.agregar_nota_track(0, 36, 2.0, 0.5)
    s.agregar_nota_track(0, 38, 3.0, 0.25)
    
    s.agregar_nota_track(1, 36, 0.0, 1.0)
    s.agregar_nota_track(1, 36, 2.0, 1.0)
    s.agregar_nota_track(1, 41, 4.0, 1.0)
    s.agregar_nota_track(1, 43, 6.0, 1.0)
    
    s.agregar_nota_track(2, 60, 0.5, 0.25)
    s.agregar_nota_track(2, 64, 0.75, 0.25)
    s.agregar_nota_track(2, 67, 1.0, 0.25)
    s.agregar_nota_track(2, 72, 1.5, 0.5)
    s.agregar_nota_track(2, 60, 2.5, 0.25)
    s.agregar_nota_track(2, 64, 2.75, 0.25)
    s.agregar_nota_track(2, 67, 3.0, 0.25)
    s.agregar_nota_track(2, 71, 3.5, 0.5)
    
    s.agregar_nota_track(3, 60, 0.0, 2.0)
    s.agregar_nota_track(3, 64, 0.0, 2.0)
    s.agregar_nota_track(3, 67, 0.0, 2.0)
    s.agregar_nota_track(3, 60, 4.0, 2.0)
    s.agregar_nota_track(3, 65, 4.0, 2.0)
    s.agregar_nota_track(3, 69, 4.0, 2.0)
    
    onda = s.renderizar(8.0)
    s.guardar_wav(onda, "musica/mi_cancion.wav")
    s.reproducir("musica/mi_cancion.wav")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "basico":
            ejemplo_basico()
        elif sys.argv[1] == "proyecto":
            ejemplo_proyecto()
        else:
            print("Uso: python sintetizador.py [basico|proyecto]")
    else:
        ejemplo_basico()