# -*- coding: utf-8 -*-
"""
    copyright 2008  - Johannes 'josch' Schauer <j.schauer@email.de>
    copyright 2010  - Remigiusz 'Enleth' Marcinkiewicz <enleth@enleth.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import gzip
import struct
import chardet
import binascii
#from guess_language import guessLanguage
from lxml import etree
from lxml import objectify
from bf import bf
from h3m_ids import *

def edet(string):
	e = chardet.detect(string)
	if e["encoding"] in h3m_encoding_quirks:
		e["encoding"] = h3m_encoding_quirks[e["encoding"]]
	return e

def extract(filename):
	h3m_data = gzip.open(filename)
	r = lambda s: struct.unpack(s,h3m_data.read(struct.calcsize(s)))
	E = objectify.ElementMaker(annotate=False)
	
	try:
		vver = h3m_versions[r("<I")[0]]
	except KeyError:
		raise ValueError("Invalid game version or not a HoMM 3 map")
	
	if vver == "WoG":
		raise NotImplementedError("WoG maps not supported yet")
	
	(vhas_players, vsize, vunderground) = r("<BIB");
	if vunderground not in [0,1]:
		raise ValueError("Underground specifier not in [0,1]")
	vunderground = str(bool(vunderground))
	m = E.map(version=vver,size=str(vsize),underground=vunderground)
	m.append(E.conversion_metadata())
	
	(vlength, ) = r("<I")
	if vlength>30:
		raise ValueError("Map name longer than 30 characters, possibly an invalid file")
	vname = h3m_data.read(vlength)
	enc = edet(vname)
	vname = vname.decode(enc["encoding"])
	m.append(E.name(vname))
	m.conversion_metadata.append(E.encoding(enc["encoding"],entity="/map/name[0]",confidence=str(enc["confidence"])))
	
	(vlength, ) = r("<I")
	vdesc = h3m_data.read(vlength)
	enc = edet(vdesc)
	vdesc = vdesc.decode(enc["encoding"])
	m.append(E.description(vdesc))
	m.conversion_metadata.append(E.encoding(enc["encoding"],entity="/map/description[0]",confidence=str(enc["confidence"])))
	
	try:
		vdifficulty = h3m_diffictulties[r("<B")[0]]
	except KeyError:
		raise ValueError("Invalid map difficulty value")
	m.append(E.difficulty(vdifficulty))
	
	if m.xpath("/map/@version")[0] in ["AB", "SoD", "WoG"]:
		(vmax_level,) = r("<B")
		if vmax_level==0:
			vmax_level = "Unspecified"
	else:
		vmax_level = "Unspecified"
	m.append(E.max_level(vmax_level))
	
	m.append(E.players())
	
	#player info
	for pnum in h3m_player_colors:
		(vis_human, vis_computer) = r("<BB")
		if vis_human not in [0,1] or vis_computer not in [0,1]:
			raise ValueError("Invalid player type specifiers %#04x and %#04x" % (vis_human, vis_computer))
		if vis_human == 0 and vis_computer == 0:
			#player is disabled, skipping garbage
			if m.xpath("/map/@version")[0] == "RoE":
				h3m_data.read(6)
			elif m.xpath("/map/@version")[0] == "AB":
				h3m_data.read(12)
			elif m.xpath("/map/@version")[0] in ["SoD", "WoG"]:
				h3m_data.read(13)
			m.players.append(E.player(color=h3m_player_colors[pnum],type="Disabled"))
			continue
		
		if vis_human == 1 and vis_computer == 1:
			player_type = "Both"
		elif vis_human == 1:
			player_type = "Human"
		else:
			player_type = "Computer"
		player = E.player(color=h3m_player_colors[pnum],type=player_type)
		
		try:
			vai_type = h3m_ai_types[r("<B")[0]]
		except KeyError:
			raise ValueError("Invalid AI type")
		
		player.append(E.ai(vai_type))
		
		if m.xpath("/map/@version")[0] in ["SoD", "WoG"]:
			(venforce_alignment,) = r("<B")
			if venforce_alignment not in [0,1]:
				raise ValueError("Invalid alignment enforcement specifier %#04x" % venforce_alignment)
			venforce_alignment = str(bool(venforce_alignment))
			
		else:
			venforce_alignment = "Unspecified"
		
		valignments = bf(r("<B")[0])
		
		if m.xpath("/map/@version")[0] in ["AB", "SoD", "WoG"]:
			(vconflux,) = r("<B")
			if vconflux not in [0,1]:
				raise ValueError("Invalid Conflux specifier %#04x" % vconflux)
			if vconflux == 1:
				valignments[8] = 1
		
		(vrandom_alignment,) = r("<B")
		if vrandom_alignment not in [0,1]:
			raise ValueError("Invalid random alignment specifier %#04x" % vrandom_alignment)
		if vrandom_alignment == 1:
			valignments[9] = 1
				
		alignments = set()
		for i in range(0,10):
			if valignments[i] == 1:
				alignments.add(h3m_alignments[i+1])
				
		player.append(E.alignment(', '.join(alignments),enforced=venforce_alignment))
		
		(vmain_town,) = r("<B")
		if vmain_town not in [0,1]:
			raise ValueError("Invalid main town specifier %#04x" % vmain_town)
		if vmain_town:
			if m.xpath("/map/@version")[0] in ["AB", "SoD", "WoG"]:
				(vmain_town_generate_hero, vmain_town_unknown1) = r("<BB")
				vmain_town_unknown1 = ("%#04x" % vmain_town_unknown1)
				m.conversion_metadata.append(E.unknown1(vmain_town_unknown1,player_color=h3m_player_colors[pnum]))
				if vmain_town_generate_hero not in [0,1]:
					raise ValueError("Invalid main town hero generation specifier %#04x" % vmain_town_generate_hero)
				vmain_town_generate_hero = str(bool(vmain_town_generate_hero))
			else:
				vmain_town_generate_hero = "Unspecified"
				vmain_town_unknown1 = "Unspecified"
			vcoords = r("<BBB")
			
			player.append(E.main_town("%d,%d,%d" % vcoords, generate_hero=vmain_town_generate_hero, unknown1=vmain_town_unknown1))
		
		(vgenerate_random_hero, vmain_hero) = r("<BB");
		if vgenerate_random_hero not in [0,1]:
			raise ValueError("Invalid random hero generation specifier %#04x" % vgenerate_random_hero)
		vgenerate_random_hero = str(bool(vgenerate_random_hero))
		player.append(E.generate_random_hero(vgenerate_random_hero))
		
		if vmain_hero != 0xFF:
			(vmain_hero_portrait, ) = r("<B")
			if vmain_hero_portrait == 0xFF:
				vmain_hero_portrait = "Standard"
			else:
				vmain_hero_portrait = str(vmain_hero_portrait)
			(vlength, ) = r("<I")
			vmain_hero_name = h3m_data.read(vlength)
			player.append(E.main_hero(str(vmain_hero),portrait=vmain_hero_portrait,name=vmain_hero_name))
		
		if m.xpath("/map/@version")[0] in ["AB", "SoD", "WoG"]:
			(vhero_placeholders,vheroes_count) = r("<BI")
			player.append(E.hero_placeholders(vhero_placeholders));
			if vheroes_count > 0:
				player.append(E.heroes())
				for i in range(vheroes_count):
					(vhero_portrait, ) = r("<B")
					if vhero_portrait == 0xFF:
						vhero_portrait = "Standard"
					else:
						vhero_portrait = str(vhero_portrait)
					(vlength, ) = r("<I")
					vhero_name = h3m_data.read(vlength)
					player.heroes.append(E.hero(portrait=vhero_portrait,name=vhero_name))
		
		m.players.append(player)
	
	#special victory condition
	(vvictory_condition,) = r("<B")
	try:
		vvictory_condition = h3m_victory_conditions[vvictory_condition]
	except KeyError:
		raise ValueError("Invalid special victory condition %#04x" % vvictory_condition)
	
	if vvictory_condition != "None":
		(vvictory_allow_normal, vvictory_apply_to_computer) = r("<BB")		
		if vvictory_allow_normal not in [0,1]:
			raise ValueError("Invalid normal victory specifier %#04x" % vvictory_allow_normal)
		if vvictory_apply_to_computer not in [0,1]:
			raise ValueError("Invalid special victory for computer specifier %#04x" % vvictory_apply_to_computer)
		vvictory_allow_normal = str(bool(vvictory_allow_normal))
		vvictory_apply_to_computer = str(bool(vvictory_apply_to_computer))
		m.append(E.special_victory_condition(type=vvictory_condition, allow_normal=vvictory_allow_normal, apply_to_computer=vvictory_apply_to_computer))
		
		if vvictory_condition == "Acquire artifact":
			(vvictory_artifact_id,) = r("<B")
			try:
				vvictory_artifact_id = h3m_artifact_types[vvictory_artifact_id]
			except KeyError:
				raise ValueError("Invalid special victory artifact id %#04x" % vvictory_artifact_id)
			m.special_victory_condition.append(E.artifact(vvictory_artifact_id))
			
			if m.xpath("/map/@version")[0] in ["AB", "SoD", "WoG"]:
				(vvictory_artifact_unknown2,) = r("<B")
				vvictory_artifact_unknown2 = ("%#04x" % vvictory_artifact_unknown2)
				m.special_victory_condition.append(E.unknown2(vvictory_artifact_unknown2))
				m.conversion_metadata.append(E.unknown2(vvictory_artifact_unknown2))
		elif vvictory_condition == "Accumulate creatures":
			(vvictory_creature_id,vvictory_creature_quantity) = r("<BI")
			try:
				vvictory_creature_id = h3m_creature_types[vvictory_creature_id]
			except KeyError:
				raise ValueError("Invalid special victory creature id %#04x" % vvictory_creature_id)
			m.special_victory_condition.append(E.creature(vvictory_creature_id,quantity=str(vvictory_creature_quantity)))
		elif vvictory_condition == "Accumulate resources":
			(vvictory_resource_type, vvictory_resource_quantity) = r("<BI")
			try:
				vvictory_resource_type = h3m_resource_types[vvictory_resource_type]
			except KeyError:
				raise ValueError("Invalid special victory resource type %#04x" % vvictory_resource_type)
			m.special_victory_condition.append(E.resource(vvictory_resource_type,quantity=str(vvictory_resource_quantity)))
		elif vvictory_condition == "Upgrade town":
			raise NotImplementedError
		elif vvictory_condition in ("Build Grail", "Defeat hero", "Capture town", "Defeat monster"):
			vcoords = r("<BBB")
			m.special_victory_condition.append(E.location("%d,%d,%d" % vcoords))
		elif vvictory_condition in ("Flag all dwellings", "Flag all mines"):
			pass
		elif vvictory_condition == "Transport artifact":
			raise NotImplementedError
		else:
			raise NotImplementedError
	
	#special loss condition
	(vloss_condition,) = r("<B")
	try:
		vloss_condition = h3m_loss_conditions[vloss_condition]
	except KeyError:
		raise ValueError("Invalid special loss condition %#04x" % vloss_condition)
	
	if vloss_condition != "None":
		m.append(E.special_loss_condition(type=vloss_condition))
		if vloss_condition in ("Lose town", "Lose hero"):
			vcoords = r("<BBB")
			m.special_loss_condition.append(E.location("%d,%d,%d" % vcoords))
		elif vloss_condition == "Time limit":
			(vloss_days,) = r("<H")
			m.special_loss_condition.append(E.days(str(vloss_days)))
		else:
			raise NotImplementedError
	
	#Teams
	(vteam_count, ) = r("<B")
	if vteam_count > 0:
		#print dict(zip(range(0,8),r("<8B")))
		vteams = r("<8B")
		for pnum in range(0,8):
			if m.xpath("/map/players/player[@color=$color]/@type",color=h3m_player_colors[pnum])[0] != "Disabled":
				m.xpath("/map/players/player[@color=$color]",color=h3m_player_colors[pnum])[0].append(E.team(str(vteams[pnum])))
		
	#guess_str = m.xpath("/map/name")[0].text + ' ' + m.xpath("/map/description")[0].text
	#print guessLanguage(guess_str)
	
	if m.xpath("/map/@version")[0] == "RoE":
		vavailable_heroes = r("<16s")[0]
	else:
		vavailable_heroes = r("<20s")[0]
		vunknown3 = "0x"+binascii.hexlify(r("<4s")[0])
		m.conversion_metadata.append(E.unknown3(vunknown3))
	
	if m.xpath("/map/@version")[0] in ["SoD", "WoG"]:
		(vdisposed_heroes,) = r("<B")
		if vdisposed_heroes != 0:
			raise NotImplementedError("Disposed heroes not implemented")
	
	vunknown4 = "0x"+binascii.hexlify(r("<31s")[0])
	m.conversion_metadata.append(E.unknown4(vunknown4))
	
	if m.xpath("/map/@version")[0] == "AB":
		vavailable_artifacts = r("<17s")[0]
	elif m.xpath("/map/@version")[0] in ["SoD", "WoG"]:
		vavailable_artifacts = r("<18s")[0]
	
	if m.xpath("/map/@version")[0] in ["SoD", "WoG"]:
		vavailable_spells = r("<9s")[0]
	
	if m.xpath("/map/@version")[0] in ["SoD", "WoG"]:
		vavailable_skills = r("<4s")[0]
	
	(vrumors_count,) = r("<B");
	vunknown5 = "0x"+binascii.hexlify(r("<3s")[0])
	m.conversion_metadata.append(E.unknown5(vunknown5))
	for rnum in range(vrumors_count):
		(vlength, ) = r("<I")
		vrumor_name = h3m_data.read(vlength)
		enc = edet(vrumor_name)
		vrumor_name = vrumor_name.decode(enc["encoding"])
		#m.conversion_metadata.append(E.encoding(enc["encoding"],entity="/map/rumor[@name='']",confidence=str(enc["confidence"])))
		(vlength, ) = r("<I")
		vrumor_text = h3m_data.read(vlength)
		enc = edet(vrumor_text)
		vrumor_text = vrumor_text.decode(enc["encoding"])
		m.append(E.rumor(vrumor_text,name=vrumor_name))
		#m.conversion_metadata.append(E.encoding(enc["encoding"],entity="/map/description[0]",confidence=str(enc["confidence"])))
		
	
		
	
	#(map_data["heroes_count"], ) = struct.unpack("<B", h3m_data.read(1))
	#if map_data["heroes_count"] > 0:
		#map_data["free_heroes"] = []
		#for i in range(map_data["heroes_count"]):
			#(hero_id, ) = struct.unpack("<B", h3m_data.read(1))
			#(hero_portrait, ) = struct.unpack("<B", h3m_data.read(1))
			#(name_length, ) = struct.unpack("<I", h3m_data.read(4))
			#hero_name = h3m_data.read(name_length)
			#(hero_players, ) = struct.unpack("<B", h3m_data.read(1))
			#map_data["free_heroes"].append({"id": hero_id, "portrait":hero_portrait, "name":hero_name, "players":hero_players})
	
	#hero options
	#for i in range(156):
		#(hero_enable, ) = struct.unpack("<B", h3m_data.read(1))
		#if hero_enable == 1:
			#(isExp, ) = struct.unpack("<B", h3m_data.read(1))
			#if isExp == 0x01:
				#(exp, ) = struct.unpack("<I", h3m_data.read(4))
			#(isSecSkill, ) = struct.unpack("<B", h3m_data.read(1))
			#if isSecSkill == 0x01:
				#(skills_count, ) = struct.unpack("<I", h3m_data.read(4))
				#for i in range(skills_count):
					#(skill_id, ) = struct.unpack("<B", h3m_data.read(1))
					#(skill_lvl, ) = struct.unpack("<B", h3m_data.read(1))
			#(isArtifact, ) = struct.unpack("<B", h3m_data.read(1))
			#if isArtifact == 0x01:
				#raise NotImplementedError
			#(isBiography, ) = struct.unpack("<B", h3m_data.read(1))
			#if isBiography == 0x01:
				#(length, ) = struct.unpack("<I", h3m_data.read(4))
				#biography = h3m_data.read(length)
			#(gender, ) = struct.unpack("<B", h3m_data.read(1))
			#(isSpells, ) = struct.unpack("<B", h3m_data.read(1))
			#if isSpells == 0x01:
				#spells = struct.unpack("<9B", h3m_data.read(9))
			#(isPrimarySkills, ) = struct.unpack("<B", h3m_data.read(1))
			#if isPrimarySkills == 0x01:
				#(attack, defense, power, knowledge) = struct.unpack("<4B", h3m_data.read(4))
	
	if m.xpath("/map/@version")[0] in ["SoD", "WoG"]:
		vunknown6 = "0x"+binascii.hexlify(r("<156s")[0])
		m.conversion_metadata.append(E.unknown6(vunknown6))
	
	
	map_size = int(m.xpath("/map/@size")[0])
	upper_terrain = [[] for i in range(map_size)]
	#read upper world
	for i in range(map_size**2):
		x = i%map_size
		y = (i-x)/map_size
		upper_terrain[y].append(r("<7B"))
	
	#read underworld
	if m.xpath("/map/@underground")[0] == "True":
		lower_terrain = [[] for i in range(map_size)]
		for i in range(map_size**2):
			x = i%map_size
			y = (i-x)/map_size
			lower_terrain[y].append(r("<7B"))
	
	
	(vdef_count, ) = r("<I")
	print vdef_count
	defs = []
	for i in range(vdef_count):
		(vlength, ) = r("<I")
		vdef_filename = h3m_data.read(vlength)
		#the biggest object is 8x6 tiles big - this is an array that maps
		#passability to each of this tiles with bits 1 passable, 0 not passable
		#we store a set with all not passable tiles
		print vdef_filename
		vdef_passability = r("<6B") #passability
		vdef_passability = frozenset([(8-x,6-y) for x in range(8)
										for y, p in enumerate(vdef_passability)
										if not (p >> x) & 1])
		vdef_accessibility = r("<6B") #passability
		vdef_accessibility = frozenset([(8-x,6-y) for x in range(8)
										for y, p in enumerate(vdef_accessibility)
										if not (p >> x) & 1])
		h3m_data.read(2) #landscape
		h3m_data.read(2) #land_edit_groups
		(vdef_type,vdef_subtype,vdef_groups,vdef_underlay ) = r("<IIBB")
		h3m_data.read(16) #junk

	return m
	(vobj_count, ) = r("<I")
	
	map_data["tunedobj"] = []
	for i in range(map_data["tunedobj_count"]):
		(x, y, z) = struct.unpack("<3B", h3m_data.read(3))
		(object_id, ) = struct.unpack("<I", h3m_data.read(4))
		#print x,y,z,object_id,
		junk = h3m_data.read(5) #junk
		#if junk != "\x00\x00\x00\x00\x00":
		#    for c in junk:
		#        print("%02d"%ord(c), end=' ')
		#    break
		#print i, map_data["objects"][object_id]["filename"],
		#print map_data["objects"][object_id]["class"]
		
		map_data["tunedobj"].append({"id":object_id, "x":x, "y":y, "z":z})
		
		if object_id in (0,1):
			pass
		elif map_data["objects"][object_id]["class"] == 53:
			if map_data["objects"][object_id]["number"] == 7:
				h3m_data.read(4)
			else:
				h3m_data.read(4)
		elif map_data["objects"][object_id]["class"] in (76, 79):
			(isText, ) = struct.unpack("<B", h3m_data.read(1))
			if isText == 0x01:
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				text = h3m_data.read(length)
				(isGuards, ) = struct.unpack("<B", h3m_data.read(1))
				if isGuards == 0x01:
					for i in range(7):
						(guard_id, guard_count) = struct.unpack("<HH", h3m_data.read(4))
				h3m_data.read(4) #junk
			(quantity, ) = struct.unpack("<I", h3m_data.read(4))
			h3m_data.read(4) #junk
		elif map_data["objects"][object_id]["class"] in (34, 70, 62):
			(hero_id, color, hero) = struct.unpack("<IBB", h3m_data.read(6))
			(isName, ) = struct.unpack("<B", h3m_data.read(1))
			if isName == 0x01:
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				name = h3m_data.read(length)
			(isExp, ) = struct.unpack("<B", h3m_data.read(1))
			if isExp == 0x01:
				(exp, ) = struct.unpack("<I", h3m_data.read(4))
			(isPortrait, ) = struct.unpack("<B", h3m_data.read(1))
			if isPortrait == 0x01:
				(portrait, ) = struct.unpack("<B", h3m_data.read(1))
			(isSecSkill, ) = struct.unpack("<B", h3m_data.read(1))
			if isSecSkill == 0x01:
				(skills_count, ) = struct.unpack("<I", h3m_data.read(4))
				for i in range(skills_count):
					(skill_id, ) = struct.unpack("<B", h3m_data.read(1))
					(skill_lvl, ) = struct.unpack("<B", h3m_data.read(1))
			(isCreature, ) = struct.unpack("<B", h3m_data.read(1))
			if isCreature == 0x01:
				for i in range(7):
					(guard_id, ) = struct.unpack("<H", h3m_data.read(2))
					(guard_count, ) = struct.unpack("<H", h3m_data.read(2))
			(creaturesFormation, ) = struct.unpack("<B", h3m_data.read(1))
			(isArtifact, ) = struct.unpack("<B", h3m_data.read(1))
			if isArtifact == 0x01:
				(headID, shouldersID, neckID, rightHandID, leftHandID, 
				trunkID, rightRingID, leftRingID, legsID, misc1ID, misc2ID,
				misc3ID, misc4ID, machine1ID, machine2ID, machine3ID,
				machine4ID, magicbook, misc5ID) \
					= struct.unpack("<19H", h3m_data.read(38))
				(knapsack_count, ) = struct.unpack("<H", h3m_data.read(2))
				if knapsack_count > 0:
					for i in range(knapsack_count):
						(knapsackID, ) = struct.unpack("<H", h3m_data.read(2))
			(zoneRadius, ) = struct.unpack("<B", h3m_data.read(1))
			(isBiography, ) = struct.unpack("<B", h3m_data.read(1))
			if isBiography == 0x01:
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				biography = h3m_data.read(length)
			(gender, ) = struct.unpack("<B", h3m_data.read(1))
			(isSpells, ) = struct.unpack("<B", h3m_data.read(1))
			if isSpells == 0x01:
				spells = struct.unpack("<9B", h3m_data.read(9))
			(isPrimarySkills, ) = struct.unpack("<B", h3m_data.read(1))
			if isPrimarySkills == 0x01:
				(attack, defense, power, knowledge) = struct.unpack("<4B", h3m_data.read(4))
			h3m_data.read(16) #unknown
		elif map_data["objects"][object_id]["class"] in (17, 20, 42):
			(owner, ) = struct.unpack("<I", h3m_data.read(4))
		elif map_data["objects"][object_id]["class"] == 93:
			(isText, ) = struct.unpack("<B", h3m_data.read(1))
			if isText == 0x01:
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				text = h3m_data.read(length)
				(isGuards, ) = struct.unpack("<B", h3m_data.read(1))
				if isGuards == 0x01:
					for i in range(7):
						(guard_id, guard_count) = struct.unpack("<HH", h3m_data.read(4))
				h3m_data.read(4) #junk
			(spell_id, ) = struct.unpack("<I", h3m_data.read(4))
		elif map_data["objects"][object_id]["class"] == 216:
			(owner, ) = struct.unpack("<I", h3m_data.read(4))
			(junk, ) = struct.unpack("<I", h3m_data.read(4))
			if junk == 0x00:
				(towns, ) = struct.unpack("<H", h3m_data.read(2))
			(minlevel, maxlevel, ) = struct.unpack("<2B", h3m_data.read(2))
		elif map_data["objects"][object_id]["class"] in (54, 71, 72, 73, 74, 75, 162, 163, 164):
			(monster_id, ) = struct.unpack("<I", h3m_data.read(4))
			(monster_count, ) = struct.unpack("<H", h3m_data.read(2))
			(mood, ) = struct.unpack("<B", h3m_data.read(1))
			(isTreasureOrText, ) = struct.unpack("<B", h3m_data.read(1))
			if isTreasureOrText == 0x01:
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				text = h3m_data.read(length)
				(wood, mercury, ore, sulfur, crystal, gem, gold, artefactID) \
					= struct.unpack("<7IH", h3m_data.read(30))
			(mosterNeverRunAway, ) = struct.unpack("<B", h3m_data.read(1))
			(monsterDontGrowUp, ) = struct.unpack("<B", h3m_data.read(1))
			h3m_data.read(2) #junk
		elif map_data["objects"][object_id]["class"] in (98, 77):
			h3m_data.read(4) #junk
			(owner, ) = struct.unpack("<B", h3m_data.read(1))
			(isName, ) = struct.unpack("<B", h3m_data.read(1))
			if isName == 0x01:
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				name = h3m_data.read(length)
			(isGuard, ) = struct.unpack("<B", h3m_data.read(1))
			if isGuard == 0x01:
				for i in range(7):
					(guard_id, guard_count) = struct.unpack("<HH", h3m_data.read(4))
			(formation, ) = struct.unpack("<B", h3m_data.read(1))
			(isBuildings, ) = struct.unpack("<B", h3m_data.read(1))
			if isBuildings == 0x01:
				build = struct.unpack("6B", h3m_data.read(6))
				active = struct.unpack("6B", h3m_data.read(6))
			else:
				(isFort, ) = struct.unpack("<B", h3m_data.read(1))
			mustSpells = struct.unpack("<9B", h3m_data.read(9))
			canSpells = struct.unpack("<9B", h3m_data.read(9))
			(eventQuantity, ) = struct.unpack("<I", h3m_data.read(4))
			if eventQuantity > 0:
				for i in range(eventQuantity):
					(length, ) = struct.unpack("<I", h3m_data.read(4))
					event_name = h3m_data.read(length)
					(length, ) = struct.unpack("<I", h3m_data.read(4))
					event_text = h3m_data.read(length)
					(wood, mercury, ore, sulfur, crystal, gem, gold, 
					players_affected, human_affected, ai_affected, 
					day_of_first_event, event_iteration) \
						= struct.unpack("<7I3B2H", h3m_data.read(35))
					h3m_data.read(16) #junk
					buildings = struct.unpack("<6B", h3m_data.read(6))
					creatures = struct.unpack("<7H", h3m_data.read(14))
					h3m_data.read(4) #junk
			h3m_data.read(4) #junk
		elif map_data["objects"][object_id]["class"] in (5, 65, 66, 67, 68, 69):
			(isText, ) = struct.unpack("<B", h3m_data.read(1))
			if isText == 0x01:
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				text = h3m_data.read(length)
				(isGuards, ) = struct.unpack("<B", h3m_data.read(1))
				if isGuards == 0x01:
					for i in range(7):
						(guard_id, guard_count) = struct.unpack("<HH", h3m_data.read(4))
				h3m_data.read(4) #junk
		elif map_data["objects"][object_id]["class"] in (33, 219):
			(color, ) = struct.unpack("<I", h3m_data.read(4))
			for i in range(7):
				(guard_id, guard_count) = struct.unpack("<HH", h3m_data.read(4))
			(undeleteSoldiers, ) = struct.unpack("<B", h3m_data.read(1))
			h3m_data.read(8)
		elif map_data["objects"][object_id]["class"] == 87:
			(owner, ) = struct.unpack("<I", h3m_data.read(4))
		elif map_data["objects"][object_id]["class"] == 83:
			(quest, ) = struct.unpack("<B", h3m_data.read(1))
			
			if quest == 0x00:
				pass
			elif quest == 0x01:
				(level, ) = struct.unpack("<I", h3m_data.read(4))
			elif quest == 0x02:
				(offence, defence, power, knowledge) = struct.unpack("4B", h3m_data.read(4))
			elif quest == 0x03:
				(hero_id, ) = struct.unpack("<I", h3m_data.read(4))
			elif quest == 0x04:
				(monster_id, ) = struct.unpack("<I", h3m_data.read(4))
			elif quest == 0x05:
				(art_quantity, ) = struct.unpack("<B", h3m_data.read(1))
				for i in range(art_quantity):
					(art, ) = struct.unpack("<H", h3m_data.read(2))
			elif quest == 0x06:
				(creatures_quantity, ) = struct.unpack("<B", h3m_data.read(1))
				for i in range(creatures_quantity):
					(guard_id, ) = struct.unpack("<H", h3m_data.read(2))
					(guard_count, ) = struct.unpack("<H", h3m_data.read(2))
			elif quest == 0x07:
				resources = struct.unpack("7I", h3m_data.read(28))
			elif quest == 0x08:
				(hero_id, ) = struct.unpack("<B", h3m_data.read(1))
			elif quest == 0x09:
				(player, ) = struct.unpack("<B", h3m_data.read(1))
			else:
				raise NotImplementedError
			
			if quest:
				(time_limit, ) = struct.unpack("<I", h3m_data.read(4))
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				quest_begin = h3m_data.read(length)
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				quest_running = h3m_data.read(length)
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				quest_end = h3m_data.read(length)
			
			(reward, ) = struct.unpack("<B", h3m_data.read(1))
			if reward == 0x00:
				pass
			elif reward == 0x01:
				(exp, ) = struct.unpack("<I", h3m_data.read(4))
			elif reward == 0x02:
				(spell_points, ) = struct.unpack("<I", h3m_data.read(4))
			elif reward == 0x03:
				(morale, ) = struct.unpack("<B", h3m_data.read(1))
			elif reward == 0x04:
				(lucky, ) = struct.unpack("<B", h3m_data.read(1))
			elif reward == 0x05:
				(resID, ) = struct.unpack("<B", h3m_data.read(1))
				(res_quantity, ) = struct.unpack("<I", h3m_data.read(4))
			elif reward == 0x06:
				(priSkillID, ) = struct.unpack("<B", h3m_data.read(1))
				(priSkillBonus, ) = struct.unpack("<B", h3m_data.read(1))
			elif reward == 0x07:
				(secSkillID, ) = struct.unpack("<B", h3m_data.read(1))
				(secSkillBonus, ) = struct.unpack("<B", h3m_data.read(1))
			elif reward == 0x08:
				(artID, ) = struct.unpack("<H", h3m_data.read(2))
			elif reward == 0x09:
				(spellID, ) = struct.unpack("<B", h3m_data.read(1))
			elif reward == 0x0A:
				(creatureID, ) = struct.unpack("<H", h3m_data.read(2))
				(creatureQuantity, ) = struct.unpack("<H", h3m_data.read(2))
			else:
				raise NotImplementedError
			
			h3m_data.read(2) #junk
		elif map_data["objects"][object_id]["class"] in (91, 59):
			(length, ) = struct.unpack("<I", h3m_data.read(4))
			text = h3m_data.read(length)
			h3m_data.read(4) #junk
		elif map_data["objects"][object_id]["class"] == 113:
			(secSkills, ) = struct.unpack("<I", h3m_data.read(4))
		elif map_data["objects"][object_id]["class"] in (88, 89, 90):
			(spellID, ) = struct.unpack("<I", h3m_data.read(4))
		elif map_data["objects"][object_id]["class"] == 215:
			(quest, ) = struct.unpack("<B", h3m_data.read(1))
			
			if quest == 0x00:
				pass
			elif quest == 0x01:
				(level, ) = struct.unpack("<I", h3m_data.read(4))
			elif quest == 0x02:
				(offence, defence, power, knowledge) = struct.unpack("4B", h3m_data.read(4))
			elif quest == 0x03:
				(hero_id, ) = struct.unpack("<I", h3m_data.read(4))
			elif quest == 0x04:
				(monster_id, ) = struct.unpack("<I", h3m_data.read(4))
			elif quest == 0x05:
				(art_quantity, ) = struct.unpack("<B", h3m_data.read(1))
				for i in range(art_quantity):
					(art, ) = struct.unpack("<H", h3m_data.read(2))
			elif quest == 0x06:
				(creatures_quantity, ) = struct.unpack("<B", h3m_data.read(1))
				for i in range(creatures_quantity):
					(guard_id, ) = struct.unpack("<H", h3m_data.read(2))
					(guard_count, ) = struct.unpack("<H", h3m_data.read(2))
			elif quest == 0x07:
				resources = struct.unpack("7I", h3m_data.read(28))
			elif quest == 0x08:
				(hero_id, ) = struct.unpack("<B", h3m_data.read(1))
			elif quest == 0x09:
				(player, ) = struct.unpack("<B", h3m_data.read(1))
			else:
				raise NotImplementedError
			
			if quest:
				(time_limit, ) = struct.unpack("<I", h3m_data.read(4))
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				quest_begin = h3m_data.read(length)
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				quest_running = h3m_data.read(length)
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				quest_end = h3m_data.read(length)
		elif map_data["objects"][object_id]["class"] == 36:
			(radius, ) = struct.unpack("<B", h3m_data.read(1))
			h3m_data.read(3) #junk
		elif map_data["objects"][object_id]["class"] == 220:
			(resources, ) = struct.unpack("<B", h3m_data.read(1))
			h3m_data.read(3) #junk
		elif map_data["objects"][object_id]["class"] == 217:
			(owner, towns) = struct.unpack("<II", h3m_data.read(8))
			if towns==0x00:
				(towns,) = struct.unpack("<H", h3m_data.read(2))
		elif map_data["objects"][object_id]["class"] == 218:
			(owner, minlvl, maxlvl) = struct.unpack("<IBB", h3m_data.read(6))
		elif map_data["objects"][object_id]["class"] == 81:
			(bonus_type, primaryID) = struct.unpack("<BI", h3m_data.read(5))
			h3m_data.read(3) #junk
		elif map_data["objects"][object_id]["class"] == 6:
			(isText, ) = struct.unpack("<B", h3m_data.read(1))
			if isText == 0x01:
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				text = h3m_data.read(length)
				(isGuards, ) = struct.unpack("<B", h3m_data.read(1))
				if isGuards == 0x01:
					for i in range(7):
						(guard_id, guard_count) = struct.unpack("<HH", h3m_data.read(4))
				h3m_data.read(4) #junk
			(exp, spell_points, morals, luck, wood, mercury, ore, sulfur,
			crystal, gem, gold, offence, defence, power, knowledge) = \
				struct.unpack("<IIBBIIIIIIIBBBB", h3m_data.read(42))
			(secSkills, ) = struct.unpack("<B", h3m_data.read(1))
			if secSkills > 0:
				for i in range(secSkills):
					(skill_id, skill_lvl) = struct.unpack("<BB", h3m_data.read(2))
			(artefacts, ) = struct.unpack("<B", h3m_data.read(1))
			if artefacts > 0:
				for i in range(artefacts):
					(artID, ) = struct.unpack("<H", h3m_data.read(2))
			(spells, ) = struct.unpack("<B", h3m_data.read(1))
			if spells > 0:
				for i in range(spells):
					(spellID, ) = struct.unpack("<B", h3m_data.read(1))
			(monsters, ) = struct.unpack("<B", h3m_data.read(1))
			if monsters > 0:
				for i in range(monsters):
					(guard_id, guard_count) = struct.unpack("<HH", h3m_data.read(4))
			h3m_data.read(8) #junk
		elif map_data["objects"][object_id]["class"] == 26:
			(isText, ) = struct.unpack("<B", h3m_data.read(1))
			if isText == 0x01:
				(length, ) = struct.unpack("<I", h3m_data.read(4))
				text = h3m_data.read(length)
				(isGuards, ) = struct.unpack("<B", h3m_data.read(1))
				if isGuards == 0x01:
					for i in range(7):
						(guard_id, guard_count) = struct.unpack("<HH", h3m_data.read(4))
				h3m_data.read(4) #junk
			(exp, spell_points, morals, luck, wood, mercury, ore, sulfur,
			crystal, gem, gold, offence, defence, power, knowledge) = \
				struct.unpack("<IIBBIIIIIIIBBBB", h3m_data.read(42))
			(secSkills, ) = struct.unpack("<B", h3m_data.read(1))
			if secSkills > 0:
				for i in range(secSkills):
					(skill_id, skill_lvl) = struct.unpack("<BB", h3m_data.read(2))
			(artefacts, ) = struct.unpack("<B", h3m_data.read(1))
			if artefacts > 0:
				for i in range(artefacts):
					(artID, ) = struct.unpack("<H", h3m_data.read(2))
			(spells, ) = struct.unpack("<B", h3m_data.read(1))
			if spells > 0:
				for i in range(spells):
					(spellID, ) = struct.unpack("<B", h3m_data.read(1))
			(monsters, ) = struct.unpack("<B", h3m_data.read(1))
			if monsters > 0:
				for i in range(monsters):
					(guard_id, guard_count) = struct.unpack("<HH", h3m_data.read(4))
			h3m_data.read(8) #junk
			(players, isAICan, disableAfterFirstDay) = struct.unpack("<BBB", h3m_data.read(3))
			h3m_data.read(4) #junk
	
	try:
		(gevents_count, ) = struct.unpack("<I", h3m_data.read(4))
		for i in range(gevents_count):
			(length, ) = struct.unpack("<I", h3m_data.read(4))
			name = h3m_data.read(length)
			(length, ) = struct.unpack("<I", h3m_data.read(4))
			text = h3m_data.read(length)
			h3m_data.read(7*4) #resources
			(players_affected, ) = struct.unpack("<B", h3m_data.read(1))
			(human_affected, ) = struct.unpack("<B", h3m_data.read(1))
			(ai_affected, ) = struct.unpack("<B", h3m_data.read(1))
			(day_of_first_event,) = struct.unpack("<H", h3m_data.read(2))
			(event_iteration,) = struct.unpack("<H", h3m_data.read(2))
			h3m_data.read(16) #junk
	except:
		print("d'ough...'")
	
	h3m_data.read(124) #junk
	
	return map_data
