# Runbook — Agent Assistant Support v1.0.0

## 1. Informations générales

**Nom de l’agent :** Agent Assistant Support
**Nom technique :** agent_assistant_support_v1
**Version :** v1.0.0
**Workflow :** Versionnement1.json
**Prompt principal :** prompts/support_agent_prompt_v1.md
**Configuration LLM :** config/llm_config_v1.json
**Agent Card :** AGENT_CARD.md

---

## 2. Objectif du runbook

Ce runbook décrit les procédures opérationnelles à suivre en cas d’incident sur l’agent.

Il couvre trois volets principaux :

1. la gestion des incidents ;
2. l’activation du kill-switch ;
3. le rollback vers une version stable.

---

## 3. Description courte de l’agent

L’agent est un assistant support de premier niveau.

Il reçoit un message utilisateur décrivant un problème simple, puis retourne une réponse structurée contenant :

1. un résumé du problème ;
2. une cause probable ;
3. des actions recommandées ;
4. un niveau d’urgence ;
5. une indication sur la nécessité d’une escalade humaine.

---

## 4. Architecture du workflow

```text
Chat Input
   ↓
Prompt Template
   ↓
GroqModel / LLM
   ↓
Chat Output
```

---

## 5. Incidents possibles

| Code incident | Incident                  | Description                                                 | Gravité |
| ------------- | ------------------------- | ----------------------------------------------------------- | ------- |
| INC-001       | Réponse vide              | L’agent ne retourne aucune réponse                          | Haute   |
| INC-002       | Réponse hors sujet        | L’agent répond sans respecter le rôle support               | Moyenne |
| INC-003       | Mauvais format            | L’agent ne respecte pas les 5 sections attendues            | Moyenne |
| INC-004       | Hallucination             | L’agent invente une information technique non vérifiée      | Haute   |
| INC-005       | Indisponibilité LLM       | Le modèle ne répond pas ou retourne une erreur              | Haute   |
| INC-006       | Mauvaise urgence          | L’agent sous-estime ou surestime le niveau d’urgence        | Moyenne |
| INC-007       | Problème de prompt        | Le prompt est modifié et dégrade les réponses               | Moyenne |
| INC-008       | Problème de configuration | La température, le modèle ou les tokens sont mal configurés | Moyenne |

---

## 6. Procédure de diagnostic incident

### Étape 1 — Identifier le symptôme

Vérifier ce qui se produit :

* aucune réponse ;
* réponse lente ;
* réponse incorrecte ;
* réponse hors sujet ;
* mauvais format ;
* erreur du modèle LLM ;
* comportement différent après modification du prompt ou de la configuration.

### Étape 2 — Rejouer un test simple

Utiliser l’entrée de test suivante :

```text
J’ai un problème de wifi, la connexion coupe souvent.
```

La réponse doit contenir les 5 sections suivantes :

```text
1. Résumé du problème
2. Cause probable
3. Actions recommandées
4. Niveau d’urgence
5. Escalade humaine nécessaire : Oui/Non
```

### Étape 3 — Vérifier les fichiers versionnés

Contrôler les fichiers suivants :

```text
AGENT_CARD.md
Versionnement1.json
prompts/support_agent_prompt_v1.md
config/llm_config_v1.json
```

### Étape 4 — Vérifier l’état Git

Exécuter :

```bash
git status
```

Si des fichiers apparaissent comme modifiés, vérifier les changements avec :

```bash
git diff
```

---

## 7. Gestion des incidents

### INC-001 — Réponse vide

Actions :

1. vérifier que le nœud Chat Input est bien connecté ;
2. vérifier que le Prompt Template reçoit bien le message utilisateur ;
3. vérifier que le GroqModel / LLM dispose d’une clé API valide ;
4. vérifier que le Chat Output est connecté à la sortie du modèle ;
5. refaire un test simple.

Critère de résolution :

```text
L’agent retourne une réponse structurée non vide.
```

---

### INC-002 — Réponse hors sujet

Actions :

1. vérifier le prompt principal ;
2. s’assurer que le rôle “agent d’assistance support” est bien présent ;
3. réduire la température si nécessaire ;
4. restaurer le prompt versionné si le prompt a été modifié.

Critère de résolution :

```text
L’agent répond uniquement dans le rôle d’assistance support.
```

---

### INC-003 — Mauvais format de réponse

Actions :

1. vérifier que le prompt impose les 5 sections ;
2. tester avec l’exemple Wi-Fi ;
3. corriger le prompt si une section manque ;
4. restaurer le fichier `prompts/support_agent_prompt_v1.md` si besoin.

Critère de résolution :

```text
La réponse contient systématiquement les 5 sections attendues.
```

---

### INC-004 — Hallucination

Actions :

1. identifier l’information inventée ;
2. vérifier si le prompt demande une réponse prudente ;
3. ajouter ou renforcer une consigne de prudence ;
4. demander une escalade humaine en cas de doute ;
5. éviter toute affirmation non vérifiée.

Critère de résolution :

```text
L’agent formule les hypothèses avec prudence et recommande une escalade si nécessaire.
```

---

### INC-005 — Indisponibilité LLM

Actions :

1. vérifier la clé API ;
2. vérifier le fournisseur LLM ;
3. vérifier les quotas ;
4. tester avec un autre modèle si disponible ;
5. activer le kill-switch si l’indisponibilité bloque l’usage.

Critère de résolution :

```text
Le modèle répond à nouveau ou une procédure alternative est activée.
```

---

## 8. Kill-switch

### Définition

Le kill-switch est une procédure permettant de désactiver rapidement l’agent en cas de comportement dangereux, instable ou non conforme.

### Cas d’activation

Activer le kill-switch si :

* l’agent donne des réponses dangereuses ;
* l’agent hallucine fortement ;
* l’agent fournit des recommandations incorrectes ;
* le modèle LLM est instable ;
* une mauvaise configuration provoque des réponses non maîtrisées ;
* le workflow est utilisé hors de son périmètre.

### Procédure kill-switch manuelle

1. Arrêter l’exécution du workflow dans AgenticAI Fusion.
2. Désactiver ou déconnecter temporairement le nœud LLM.
3. Remplacer la sortie par un message statique de secours.
4. Informer l’utilisateur que l’assistance automatique est indisponible.
5. Escalader vers un humain.

### Message de secours recommandé

```text
L’assistant automatique est temporairement indisponible.
Votre demande doit être prise en charge par un conseiller humain.
Merci de réessayer plus tard ou de contacter le support.
```

### Critère de succès du kill-switch

```text
L’agent ne génère plus de réponse automatique non contrôlée.
```

---

## 9. Rollback

### Définition

Le rollback consiste à revenir à une version stable précédente du projet.

Dans ce LAB, la version stable est :

```text
v1.0.0
```

### Vérifier les tags disponibles

```bash
git tag
```

Résultat attendu :

```text
v1.0.0
```

### Revenir temporairement à la version v1.0.0

```bash
git checkout v1.0.0
```

Attention : cette commande place le projet en mode lecture d’une version taguée.

### Revenir sur la branche principale après vérification

```bash
git checkout master
```

### Restaurer un fichier précis depuis v1.0.0

Exemple pour restaurer le prompt :

```bash
git checkout v1.0.0 -- prompts/support_agent_prompt_v1.md
```

Exemple pour restaurer la configuration :

```bash
git checkout v1.0.0 -- config/llm_config_v1.json
```

Exemple pour restaurer le workflow :

```bash
git checkout v1.0.0 -- Versionnement1.json
```

Puis enregistrer la restauration :

```bash
git add .
git commit -m "Rollback to v1.0.0 stable files"
```

---

## 10. Vérification après rollback

Après rollback, exécuter :

```bash
git status
```

Puis tester l’agent avec :

```text
J’ai un problème de wifi, la connexion coupe souvent.
```

La réponse doit contenir :

```text
1. Résumé du problème
2. Cause probable
3. Actions recommandées
4. Niveau d’urgence
5. Escalade humaine nécessaire : Oui/Non
```

---

## 11. Critères de retour à la normale

L’incident est considéré comme résolu si :

* l’agent répond correctement ;
* le format de sortie est respecté ;
* aucune hallucination critique n’est observée ;
* l’utilisateur reçoit une réponse exploitable ;
* le workflow fonctionne avec la version stable ;
* le tag `v1.0.0` reste disponible.

---

## 12. Responsabilités

| Rôle               | Responsabilité                                       |
| ------------------ | ---------------------------------------------------- |
| Équipe projet      | Maintenir le workflow, le prompt et la configuration |
| Référent technique | Gérer Git, rollback et versionnement                 |
| Superviseur métier | Valider la qualité des réponses                      |
| Support humain     | Prendre en charge les cas escaladés                  |

---

## 13. Historique du runbook

| Version | Date       | Description                 |
| ------- | ---------- | --------------------------- |
| v1.0.0  | 2026-06-24 | Création du runbook initial |
