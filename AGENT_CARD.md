# Agent Card — Agent Assistant Support

## 1. Identification de l’agent

**Nom de l’agent :** Agent Assistant Support
**Nom technique :** agent_assistant_support_v1
**Version :** 1.0.0
**Statut :** Stable — version initiale
**Date de création :** 2026-06-24
**Propriétaire :** Équipe projet Agentic AI
**Plateforme :** AgenticAI Fusion / LangFlow-like

---

## 2. Objectif de l’agent

L’agent a pour objectif d’assister un utilisateur qui décrit un problème simple de support technique.

Il analyse le message utilisateur et produit une réponse structurée contenant :

1. un résumé du problème ;
2. une cause probable ;
3. des actions recommandées ;
4. un niveau d’urgence ;
5. une indication sur la nécessité ou non d’une escalade humaine.

---

## 3. Cas d’usage couvert

L’agent est destiné à traiter des demandes simples de support, par exemple :

* problème de connexion Wi-Fi ;
* lenteur Internet ;
* difficulté d’accès à un service ;
* demande d’orientation de premier niveau ;
* besoin d’assistance technique de base.

Exemple d’entrée utilisateur :

```text
J’ai un problème de wifi, la connexion coupe souvent.
```

---

## 4. Architecture du workflow

Le workflow utilisé est volontairement simple :

```text
Chat Input
   ↓
Prompt Template
   ↓
GroqModel / LLM
   ↓
Chat Output
```

### Description des nœuds

| Nœud            | Rôle                                      |
| --------------- | ----------------------------------------- |
| Chat Input      | Reçoit le message utilisateur             |
| Prompt Template | Structure la consigne envoyée au LLM      |
| GroqModel / LLM | Génère la réponse de l’agent              |
| Chat Output     | Affiche la réponse finale à l’utilisateur |

---

## 5. Entrées de l’agent

| Élément             | Description                                             |
| ------------------- | ------------------------------------------------------- |
| Message utilisateur | Texte libre décrivant le problème                       |
| Format              | Message texte                                           |
| Exemple             | “J’ai un problème de wifi, la connexion coupe souvent.” |

---

## 6. Sorties de l’agent

L’agent retourne une réponse textuelle structurée selon le format suivant :

```text
1. Résumé du problème
2. Cause probable
3. Actions recommandées
4. Niveau d’urgence
5. Escalade humaine nécessaire : Oui/Non
```

---

## 7. Prompt principal

```text
Tu es un agent d’assistance support.

Ta mission est d’aider l’utilisateur à comprendre son problème et à proposer une réponse claire, structurée et prudente.

Message utilisateur :
{input}

Réponds toujours avec la structure suivante :

1. Résumé du problème
2. Cause probable
3. Actions recommandées
4. Niveau d’urgence
5. Escalade humaine nécessaire : Oui/Non
```

---

## 8. Configuration LLM

| Paramètre       | Valeur recommandée                |
| --------------- | --------------------------------- |
| Modèle          | GroqModel ou autre LLM disponible |
| Température     | 0.2 à 0.4                         |
| Max tokens      | 500 à 1000                        |
| Streaming       | Selon disponibilité               |
| Sortie attendue | Texte structuré                   |

---

## 9. Limites connues

L’agent ne doit pas être utilisé pour :

* traiter des incidents critiques sans validation humaine ;
* remplacer un technicien support ;
* prendre des décisions opérationnelles irréversibles ;
* manipuler des données sensibles ;
* exécuter automatiquement des actions externes.

L’agent fournit une aide de premier niveau uniquement.

---

## 10. Risques identifiés

| Risque                               | Description                                          | Mesure de maîtrise                            |
| ------------------------------------ | ---------------------------------------------------- | --------------------------------------------- |
| Réponse incorrecte                   | Le LLM peut proposer une mauvaise cause probable     | Réponse prudente + escalade humaine si doute  |
| Hallucination                        | Le LLM peut inventer des informations techniques     | Prompt restrictif et format de réponse imposé |
| Mauvaise classification de l’urgence | L’agent peut sous-estimer un incident                | Champ “Niveau d’urgence” obligatoire          |
| Dépendance au modèle                 | Le comportement peut changer selon le modèle utilisé | Versionner prompt et configuration            |
| Indisponibilité LLM                  | Le modèle peut être indisponible                     | Prévoir kill-switch et rollback               |

---

## 11. Critères d’acceptation

L’agent est considéré comme fonctionnel si :

* il accepte un message utilisateur ;
* il répond dans le format imposé ;
* il ne sort pas du rôle d’assistance support ;
* il indique clairement si une escalade humaine est nécessaire ;
* il produit une réponse compréhensible et exploitable.

---

## 12. Exemple de test

### Entrée

```text
J’ai un problème de wifi, la connexion coupe souvent.
```

### Sortie attendue

```text
1. Résumé du problème
L’utilisateur signale des coupures fréquentes de la connexion Wi-Fi.

2. Cause probable
Le problème peut venir du signal Wi-Fi, du routeur, d’un éloignement de la box ou d’une saturation du réseau.

3. Actions recommandées
- Redémarrer la box.
- Se rapprocher du routeur.
- Vérifier si le problème touche un seul appareil ou plusieurs.
- Tester la connexion avec un câble Ethernet si possible.
- Vérifier les voyants de la box.

4. Niveau d’urgence
Moyen.

5. Escalade humaine nécessaire
Oui, si le problème persiste après les vérifications de base.
```

---

## 13. Historique des versions

| Version | Date       | Description                                              |
| ------- | ---------- | -------------------------------------------------------- |
| 1.0.0   | 2026-06-24 | Version initiale du workflow simple d’assistance support |
