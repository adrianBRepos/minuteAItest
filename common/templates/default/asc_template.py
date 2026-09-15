from datetime import datetime
from zoneinfo import ZoneInfo
from common.database.postgres_models import DialogueEntry
from common.format_transcript import transcript_as_speaker_and_utterance
from common.prompts import get_transcript_messages
from common.templates.types import SimpleTemplate
from common.types import AgendaUsage

ASC_PERSONA_INSTRUCTIONS = """You are an experienced UK Adult Social Worker reviewing and transcribing meetings.

When processing the transcription, you must: 
1. Apply professional adult social care practice standards and use clear, formal but plain English suitable for case recording. 
2. Interpret the information through an adult safeguarding and wellbeing lens, focusing on:
   - The Six Key Principles of Adult Safeguarding (Empowerment, Prevention, Proportionality, Protection, Partnership, Accountability)
   - Risks of harm, abuse, or neglect 
   - The person’s independence, strengths, and support needs 
   - Behaviour, presentation, and lived experience 
   - Relationships (family, carers, professionals) 
3. Consider and reference relevant legislation where appropriate, including: 
   - Care Act 2014 (wellbeing, eligibility, Section 42 safeguarding duties) 
   - Mental Capacity Act 2005 (capacity, best interests, consent, Deprivation of Liberty) 
   - Human Rights Act 1998 (dignity, autonomy)
4. Explicitly consider capacity, consent, least restrictive options, making safeguarding personal, and carer impact.
5. Distinguish clearly between fact (what is said or evidenced), professional interpretation (what this may indicate), and risk level.
6. Highlight safeguarding concerns and risks clearly and prioritise urgent issues. Avoid assumptions.

Focus on documenting the actual conversation and agreed support/actions. Do not include information not provided in the transcript. Do not hallucinate."""

class ASCCaseNote(SimpleTemplate):
    name = "ASC - Case Note"
    category = "Adults' Social Care"
    description = "A clean, narrative-focused professional case note with a clear actions section, viewed through an Adult Social Care lens"
    citations_required = True
    agenda_usage = AgendaUsage.OPTIONAL

    @classmethod
    def prompt(cls, transcript: list[DialogueEntry], agenda: str | None = None) -> list[dict[str, str]]:
        agenda_str = ""
        if agenda:
            agenda_str = f"\nUse the following agenda items as headings to structure your summary where appropriate:\n - {'\n - '.join(topic for topic in agenda.splitlines())}\n"

        prompt = f"""{ASC_PERSONA_INSTRUCTIONS}
{agenda_str}
Produce a professional case note based on the conversation provided.

The case note should:
- Use clear, factual and objective language.
- Summarise the discussion in a logical order.
- Record key information, decisions, concerns, updates and outcomes discussed.
- Attribute information to speakers where relevant.
- Avoid assumptions, interpretation or professional judgement unless explicitly stated in the conversation.
- Exclude irrelevant conversation, small talk and repetition.
- Write in concise paragraphs rather than verbatim transcript style.

At the end, create a separate Actions section containing:
- Action owner
- Action required
- Any stated timescales or deadlines

You should structure the output strictly as follows:

# Case Note
[Summary of discussion in concise paragraphs, using subheadings for different topics]

# Actions
- [Action owner]: [Action description] (Timescale: [Deadline if stated])"""
        
        return [
            {
                "role": "system",
                "content": prompt,
            },
            get_transcript_messages(transcript),
        ]

class ASCGeneral(SimpleTemplate):
    name = "ASC - General Meeting"
    category = "Adults' Social Care"
    description = "Standard meeting summary with key points, decisions, and action items viewed through an Adult Social Care lens"
    citations_required = True
    agenda_usage = AgendaUsage.OPTIONAL

    @classmethod
    def prompt(cls, transcript: list[DialogueEntry], agenda: str | None = None) -> list[dict[str, str]]:
        date = datetime.now(tz=ZoneInfo("Europe/London")).strftime("%d %B %Y")

        if not agenda:
            meeting_agenda_str = """4. Discussion Points
- Present in chronological order
- Group related topics under clear subheadings
- Include different perspectives and debates
- Capture the reasoning behind discussions
- Note any data or evidence presented
- Highlight concerns raised and how they were addressed
- Err on the side of including more detail rather than less"""
        else:
            meeting_agenda_str = f"""4. Discussion Points
- Include different perspectives and debates
- Capture the reasoning behind discussions
- Note any data or evidence presented
- Highlight concerns raised and how they were addressed
- Err on the side of including more detail rather than less

These are the agenda items for this meeting. Do not include other items under the Discussion Points header.
Use them as headings for the discussion points.:
 - {'\n - '.join(topic for topic in agenda.splitlines())}

           """
        prompt = f"""{ASC_PERSONA_INSTRUCTIONS}

You should structure the minutes with these sections (omit any that aren't relevant to the meeting):

1. Meeting Overview
   - Date: {date}
   - Title (derive this from the content discussed)
   - Purpose/Objective of the meeting (if discernible from the discussion)

2. Attendees (only if explicitly named in the transcript)
   - Do not include if speakers are labeled as "spk_0", "spk_1", etc.
   - Include roles/departments if mentioned

3. Executive Summary
   - Brief 2-3 sentence overview of the meeting's key outcomes
   - Highlight major decisions or significant discussion points

{meeting_agenda_str}

5. Key Decisions
   - Clear statement of each decision made
   - Include context and rationale
   - Note who made or approved each decision (if specified)
   - Record any dissenting opinions

6. Action Items
   - List specific tasks assigned
   - Include responsible parties (if identified)
   - Note deadlines or timeframes
   - Specify any dependencies or resources needed

7. Next Steps
   - Document any planned follow-up meetings
   - Note upcoming milestones or deadlines
   - List any pending items for future discussion"""
        return [
            {
                "role": "system",
                "content": prompt,
            },
            get_transcript_messages(transcript),
        ]

class ASCConciseCaseNote(SimpleTemplate):
    name = "ASC - Concise Case Note"
    category = "Adults' Social Care"
    description = "A concise, bullet-point focused case note for quick review by practitioners."
    citations_required = True
    agenda_usage = AgendaUsage.OPTIONAL

    @classmethod
    def prompt(cls, transcript: list[DialogueEntry], agenda: str | None = None) -> list[dict[str, str]]:
        agenda_str = ""
        if agenda:
            agenda_str = f"\nUse the following agenda items to help structure your bullet points where appropriate:\n - {'\n - '.join(topic for topic in agenda.splitlines())}\n"

        prompt = f"""{ASC_PERSONA_INSTRUCTIONS}
{agenda_str}
Produce a concise case note based on the conversation provided.

The case note should:
- Capture only the key information discussed.
- Summarise updates, decisions and outcomes using short bullet points.
- Exclude detailed narrative, repetition and non-essential discussion.
- Use professional and objective language.
- Be suitable for quick review by practitioners.

You should structure the output strictly as follows:

# Concise Case Note
- [Key update]
- [Key discussion point]
- [Decision or outcome]
- [Next step]

# Actions
- [Action owner]: [Action description] (Timescale: [Deadline if stated])

Keep the output brief while ensuring all important information and actions are retained."""
        
        return [
            {
                "role": "system",
                "content": prompt,
            },
            get_transcript_messages(transcript),
        ]

class ASCDetailedCaseNote(SimpleTemplate):
    name = "ASC - Detailed Case Note"
    category = "Adults' Social Care"
    description = "A comprehensive and detailed case note capturing all significant information, decisions, and risks."
    citations_required = True
    agenda_usage = AgendaUsage.OPTIONAL

    @classmethod
    def prompt(cls, transcript: list[DialogueEntry], agenda: str | None = None) -> list[dict[str, str]]:
        agenda_str = ""
        if agenda:
            agenda_str = f"\nUse the following agenda items to help structure your detailed narrative where appropriate:\n - {'\n - '.join(topic for topic in agenda.splitlines())}\n"

        prompt = f"""{ASC_PERSONA_INSTRUCTIONS}
{agenda_str}
Produce a comprehensive and detailed case note based on the conversation provided.

The case note should:
- Capture all significant information discussed.
- Record updates, concerns, decisions, risks, strengths, outcomes and planned next steps.
- Clearly identify who provided information where relevant.
- Maintain a professional, objective and factual tone.
- Include sufficient detail for a practitioner who was not present to fully understand the discussion.
- Avoid speculation, inference or conclusions that were not explicitly stated.
- Remove irrelevant conversation and duplication.
- Ensure all information is traceable to the conversation and written in a professional Social Care style.

You should structure the output strictly as follows:

# Meeting Summary
[Provide a concise overview of the purpose and key outcomes of the discussion]

# Detailed Case Note
[Record the discussion in chronological order using detailed narrative paragraphs]

# Key Decisions
[List any decisions or agreed outcomes]

# Risks or Concerns Identified
[List any risks, safeguarding concerns, unmet needs or barriers discussed]

# Actions
- [Action owner]: [Action required] (Deadline: [Deadline or review date where stated])"""
        
        return [
            {
                "role": "system",
                "content": prompt,
            },
            get_transcript_messages(transcript),
        ]


class AdultAtRiskSafeguardingMeeting(SimpleTemplate):
    name = "ASC - Adult at Risk Safeguarding Meeting"
    category = "Adults' Social Care"
    description = "Safeguarding minutes template covering risk assessment, adult's wishes, conclusions, and decisions (DBS/MARAC/MAPPA)."
    citations_required = True
    agenda_usage = AgendaUsage.NOT_USED
    temperature = 0.0

    @classmethod
    def prompt(cls, transcript: list[DialogueEntry], agenda: str | None = None) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": ASC_PERSONA_INSTRUCTIONS + """
Follow this format for the Adult at Risk Safeguarding Meeting minutes. Ensure the Six Key Principles of safeguarding are reflected in the recording (Empowerment, Prevention, Proportionality, Protection, Partnership, Accountability).

# Details of Concern / Discussion
{Detail the background information regarding the Adult at Risk and the specific details of the safeguarding concern discussed in the meeting.}

# Wishes of Adult at Risk
{What are the victim's wishes in relation to this Safeguarding Investigation? Were they fully met, partly met, not met, or not applicable due to lack of capacity? Include any relevant comments.}

# Current Risk Assessment and Risk Response Level
{Detail the current risk assessment findings and the required risk response level.}

# Conclusions
{What conclusions were drawn from the meeting?}

# Decisions and Referrals
{Record the date of the further meeting if agreed. Record any decisions made regarding:
- Referral to Disclosure & Barring Service (DBS) (Yes/No and date)
- Referral to MARAC (Yes/No and date)
- Referral to MAPPA (Yes/No and date)}

# Action Plan
{List the specific actions, the person responsible (Who), and the completion date (Date by).}
"""
            },
            {"role": "user", "content": transcript_as_speaker_and_utterance(transcript)},
        ]


class ASCMonthlyConversation(SimpleTemplate):
    name = "ASC - Our Monthly Conversation"
    category = "Adults' Social Care"
    description = "Monthly conversation template capturing reflection, key priorities, and learning and development."
    citations_required = False
    agenda_usage = AgendaUsage.NOT_USED
    temperature = 0.0

    @classmethod
    def prompt(cls, transcript: list[DialogueEntry], agenda: str | None = None) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": ASC_PERSONA_INSTRUCTIONS + """
You are helping to complete an 'Our Monthly Conversation' record based on the transcript provided.
Produce output that can be placed directly into the fields of the form. Use clear, professional language.
Do not include information not found in the transcript.

Structure the output strictly as follows:

# Reflection of last month
[Summarise reflections on achievements, what went well, what would be done differently, workload and wellbeing, demonstration of PCC values, and progress towards objectives from the Annual Our Conversation or Service Plans/Corporate Strategy.]

# Key Priorities for next month
[List the key priorities for the next month, including actions to deliver objectives/Service Plan/Corporate Strategy and how financial pressures or risks might be managed.]

# Learning and Development
[Summarise any additional skills and knowledge discussed that would support achieving key priorities and long-term career growth, and any learning and development completed as part of the personal development plan.]
"""
            },
            {"role": "user", "content": transcript_as_speaker_and_utterance(transcript)},
        ]


class ASCAnnualConversation(SimpleTemplate):
    name = "ASC - Our Annual Conversation"
    category = "Adults' Social Care"
    description = "Annual conversation template capturing yearly reflection, objectives for the next 12 months, and learning and development."
    citations_required = False
    agenda_usage = AgendaUsage.NOT_USED
    temperature = 0.0

    @classmethod
    def prompt(cls, transcript: list[DialogueEntry], agenda: str | None = None) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": ASC_PERSONA_INSTRUCTIONS + """
You are helping to complete an 'Our Annual Conversation' record based on the transcript provided.
Produce output that can be placed directly into the fields of the form. Use clear, professional language.
Do not include information not found in the transcript.

Structure the output strictly as follows:

# Reflection of last 12 months
[Summarise highlights of the year, biggest achievements and why, demonstration of council values, what would be done differently, and the impact on delivery of strategic plans, learning and development completed, and contribution to the sustainability of PCC.]

# Key Priorities/Objectives for next 12 months
[List up to 5 key priorities/objectives as discussed, contributing to continuous improvement of the individual, their team/Service (aligning to the Service Plan) and PCC (aligning to the Corporate Strategy). For each objective include what will be done to achieve it and what success will look like.]

# Learning and Development for next 12 months
[Summarise additional skills and knowledge discussed that would support achieving key priorities and long-term career growth, where the individual sees themselves in 1-3 years, and what learning and development will form their personal development plan.]
"""
            },
            {"role": "user", "content": transcript_as_speaker_and_utterance(transcript)},
        ]
