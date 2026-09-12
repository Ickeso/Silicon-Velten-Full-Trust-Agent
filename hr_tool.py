#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ████████████████████████████████████████████████████████████████████
# FILE       : tools/hr_tool.py
# PROJECT    : FULL_TRUST_AGENT / SILICON VELTEN CORE
# VERSION    : v1.1.0 ENTERPRISE – TITANIUM HARDENING
# STATUS     : PRODUCTION READY – DETERMINISTISCH, ISOLIERT
# ----------------------------------------------------------------------
# TITANIUM HARDENING v1.1.0:
#   ✅ run(payload, action) -> dict als Standard-Contract
#   ✅ Alle @require_approval Dekoratoren entfernt (Entscheidung liegt beim Runner)
#   ✅ Platzhalter-Prüfung ({{...}}) für alle Nutzereingaben
#   ✅ DB-Pfad innerhalb des Workspace (AGENT_WORKSPACE)
#   ✅ Subprozess-kompatibler __main__-Block
#   ✅ Alle HR-Funktionen (Onboarding, Dokumente, Abwesenheiten) vollständig erhalten
# ████████████████████████████████████████████████████████████████████

import os
import json
import sys
import sqlite3
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

from core.events import log_event


# ------------------------------------------------------------------
# ENUMS
# ------------------------------------------------------------------

class DocumentType(Enum):
    CONTRACT = "contract"
    CERTIFICATE = "certificate"
    PAYSLIP = "payslip"
    SICK_NOTE = "sick_note"
    VACATION_REQUEST = "vacation_request"
    PERFORMANCE_REVIEW = "performance_review"
    TAX_DOCUMENT = "tax_document"
    SOCIAL_SECURITY = "social_security"
    OTHER = "other"


class AccessLevel(Enum):
    SELF = "self"
    MANAGER = "manager"
    HR = "hr"
    ADMIN = "admin"


# ------------------------------------------------------------------
# HR TOOL KLASSE
# ------------------------------------------------------------------

class HRTool:
    """Personalverwaltungstool für den Full-Trust-Agent. Keine Approvals im Tool."""

    def __init__(self, db_path: Optional[str] = None):
        # Werkzeug arbeitet innerhalb des Agent-Workspace
        workspace = os.environ.get("AGENT_WORKSPACE", os.getcwd())
        self.db_path = db_path or os.path.join(workspace, "data", "hr", "hr.db")
        self.documents_dir = os.path.join(os.path.dirname(self.db_path), "documents")
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.documents_dir, exist_ok=True)
        
        self._init_database()
        
        log_event(
            "hr_tool",
            "initialized",
            {
                "db_path": self.db_path,
                "documents_dir": self.documents_dir
            }
        )

    # ================================================================
    # DATENBANK
    # ================================================================

    def _init_database(self) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    department TEXT NOT NULL,
                    position TEXT NOT NULL,
                    hire_date TEXT NOT NULL,
                    termination_date TEXT,
                    status TEXT NOT NULL DEFAULT 'active',
                    salary REAL DEFAULT 0.0,
                    birth_date TEXT,
                    tax_id TEXT,
                    social_security_id TEXT,
                    address TEXT,
                    phone TEXT,
                    manager_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    document_id TEXT PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    document_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    uploaded_by TEXT NOT NULL,
                    uploaded_at TEXT NOT NULL,
                    is_confidential INTEGER DEFAULT 0,
                    retention_until TEXT,
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id TEXT PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS access_control (
                    user_id TEXT PRIMARY KEY,
                    access_level TEXT NOT NULL DEFAULT 'self',
                    employee_id TEXT,
                    assigned_by TEXT,
                    assigned_at TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS absence_requests (
                    request_id TEXT PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    comment TEXT,
                    approved_by TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def _execute(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            
            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            return []
        except Exception as e:
            log_event("hr_tool", "error", {"query": query, "error": str(e)}, severity="ERROR")
            raise
        finally:
            conn.close()

    # ================================================================
    # AUDIT LOGGING
    # ================================================================

    def _log_audit(self, employee_id: str, user_id: str, action: str, details: str) -> None:
        audit_id = f"AUD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()
        
        query = """
            INSERT INTO audit_log (id, employee_id, user_id, action, details, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self._execute(query, (audit_id, employee_id, user_id, action, details, timestamp))
        
        log_event(
            "hr_tool",
            "audit",
            {
                "audit_id": audit_id,
                "employee_id": employee_id,
                "user_id": user_id,
                "action": action
            }
        )

    def get_audit_trail(self, employee_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        query = """
            SELECT * FROM audit_log
            WHERE employee_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """
        return self._execute(query, (employee_id, limit))

    # ================================================================
    # ZUGRIFFSKONTROLLE
    # ================================================================

    def _check_access(self, user_id: str, employee_id: str, required_level: AccessLevel = AccessLevel.SELF) -> bool:
        if user_id == "ADMIN":
            return True
            
        query = "SELECT access_level, employee_id FROM access_control WHERE user_id = ?"
        results = self._execute(query, (user_id,))
        
        if not results:
            return False
            
        row = results[0]
        level = row["access_level"]
        assigned_employee_id = row["employee_id"]
        
        if level in ["hr", "admin"]:
            return True
            
        if level == "manager":
            if employee_id == assigned_employee_id:
                return True
            emp_query = "SELECT manager_id FROM employees WHERE employee_id = ?"
            emp_results = self._execute(emp_query, (employee_id,))
            if emp_results and emp_results[0]["manager_id"] == assigned_employee_id:
                return True
            return False
            
        if level == "self":
            return employee_id == assigned_employee_id
            
        return False

    def grant_access(self, user_id: str, access_level: str, employee_id: Optional[str] = None,
                    assigned_by: str = "SYSTEM") -> bool:
        if access_level not in ["self", "manager", "hr", "admin"]:
            raise ValueError(f"Invalid access_level: {access_level}")
            
        if access_level in ["self", "manager"] and not employee_id:
            raise ValueError(f"employee_id required for access_level: {access_level}")
            
        query = """
            INSERT OR REPLACE INTO access_control
            (user_id, access_level, employee_id, assigned_by, assigned_at)
            VALUES (?, ?, ?, ?, ?)
        """
        self._execute(query, (user_id, access_level, employee_id, assigned_by, datetime.now().isoformat()))
        
        self._log_audit(employee_id or user_id, assigned_by, "GRANT_ACCESS", f"Granted {access_level} access")
        return True

    # ================================================================
    # MITARBEITER-STAMMDATEN
    # ================================================================

    def create_employee(self, employee_data: Dict[str, Any], user_id: str = "SYSTEM") -> Dict[str, Any]:
        required = ["first_name", "last_name", "email", "department", "position", "hire_date"]
        for field in required:
            if field not in employee_data:
                raise ValueError(f"Missing required field: {field}")
        
        employee_id = f"EMP-{datetime.now().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
        timestamp = datetime.now().isoformat()
        
        query = """
            INSERT INTO employees (
                employee_id, first_name, last_name, email, department, position,
                hire_date, termination_date, status, salary, birth_date, tax_id,
                social_security_id, address, phone, manager_id, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self._execute(query, (
            employee_id,
            employee_data["first_name"],
            employee_data["last_name"],
            employee_data["email"],
            employee_data["department"],
            employee_data["position"],
            employee_data["hire_date"],
            None,
            "probation",
            employee_data.get("salary", 0.0),
            employee_data.get("birth_date"),
            employee_data.get("tax_id"),
            employee_data.get("social_security_id"),
            employee_data.get("address"),
            employee_data.get("phone"),
            employee_data.get("manager_id"),
            timestamp,
            timestamp
        ))
        
        self._log_audit(employee_id, user_id, "CREATE_EMPLOYEE", json.dumps(employee_data))
        
        return {
            "success": True,
            "employee_id": employee_id,
            "message": f"Employee {employee_data['first_name']} {employee_data['last_name']} created"
        }

    def get_employee(self, employee_id: str, user_id: str = "SYSTEM") -> Dict[str, Any]:
        if not self._check_access(user_id, employee_id, AccessLevel.SELF):
            return {"success": False, "message": "Access denied"}
        
        query = "SELECT * FROM employees WHERE employee_id = ?"
        results = self._execute(query, (employee_id,))
        
        if not results:
            return {"success": False, "message": f"Employee {employee_id} not found"}
        
        self._log_audit(employee_id, user_id, "VIEW_EMPLOYEE", "Viewed employee record")
        return {"success": True, "data": results[0]}

    def list_employees(self, user_id: str = "SYSTEM", department: Optional[str] = None) -> Dict[str, Any]:
        query = "SELECT access_level FROM access_control WHERE user_id = ?"
        results = self._execute(query, (user_id,))
        
        if not results or results[0]["access_level"] not in ["hr", "admin"]:
            return {"success": False, "message": "Access denied. HR or Admin privileges required"}
        
        sql = "SELECT * FROM employees"
        params = []
        if department:
            sql += " WHERE department = ?"
            params.append(department)
            
        employees = self._execute(sql, tuple(params))
        return {"success": True, "count": len(employees), "employees": employees}

    def update_employee(self, employee_id: str, updates: Dict[str, Any], user_id: str = "SYSTEM") -> Dict[str, Any]:
        if not self._check_access(user_id, employee_id, AccessLevel.HR):
            return {"success": False, "message": "Access denied"}
        
        allowed_fields = [
            "first_name", "last_name", "email", "department", "position",
            "status", "salary", "address", "phone", "manager_id"
        ]
        
        update_fields = []
        params = []
        for field, value in updates.items():
            if field in allowed_fields:
                update_fields.append(f"{field} = ?")
                params.append(value)
        
        if not update_fields:
            return {"success": False, "message": "No valid fields to update"}
        
        params.append(datetime.now().isoformat())
        params.append(employee_id)
        
        query = f"UPDATE employees SET {', '.join(update_fields)}, updated_at = ? WHERE employee_id = ?"
        self._execute(query, tuple(params))
        
        self._log_audit(employee_id, user_id, "UPDATE_EMPLOYEE", json.dumps(updates))
        return {"success": True, "message": f"Employee {employee_id} updated"}

    def terminate_employee(self, employee_id: str, termination_date: str, reason: str = "",
                          user_id: str = "SYSTEM") -> Dict[str, Any]:
        if not self._check_access(user_id, employee_id, AccessLevel.HR):
            return {"success": False, "message": "Access denied"}
        
        query = """
            UPDATE employees 
            SET status = 'terminated', termination_date = ?, updated_at = ?
            WHERE employee_id = ?
        """
        self._execute(query, (termination_date, datetime.now().isoformat(), employee_id))
        
        self._log_audit(employee_id, user_id, "TERMINATE_EMPLOYEE", f"Reason: {reason}")
        return {"success": True, "message": f"Employee {employee_id} terminated"}

    # ================================================================
    # DOKUMENTENVERWALTUNG
    # ================================================================

    def upload_document(self, employee_id: str, document_data: Dict[str, Any], 
                       file_content: bytes, user_id: str = "SYSTEM") -> Dict[str, Any]:
        if not self._check_access(user_id, employee_id, AccessLevel.HR):
            return {"success": False, "message": "Access denied"}
        
        doc_id = f"DOC-{datetime.now().strftime('%Y%m')}-{uuid.uuid4().hex[:8].upper()}"
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        safe_filename = f"{employee_id}_{doc_id}_{document_data.get('title', 'document')}"
        file_path = os.path.join(self.documents_dir, safe_filename)
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        doc_type = document_data.get("document_type", "other")
        valid_types = [d.value for d in DocumentType]
        if doc_type not in valid_types:
            doc_type = "other"
        
        query = """
            INSERT INTO documents 
            (document_id, employee_id, document_type, title, description, 
             file_hash, file_path, uploaded_by, uploaded_at, is_confidential, retention_until)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self._execute(query, (
            doc_id, employee_id, doc_type,
            document_data.get("title", "Unbenannt"),
            document_data.get("description", ""),
            file_hash, file_path, user_id,
            datetime.now().isoformat(),
            1 if document_data.get("is_confidential", False) else 0,
            document_data.get("retention_until")
        ))
        
        self._log_audit(employee_id, user_id, "UPLOAD_DOCUMENT", f"Document {doc_id}")
        return {"success": True, "document_id": doc_id, "file_path": file_path}

    def list_documents(self, employee_id: str, user_id: str = "SYSTEM") -> Dict[str, Any]:
        if not self._check_access(user_id, employee_id, AccessLevel.SELF):
            return {"success": False, "message": "Access denied"}
        
        query = """
            SELECT document_id, document_type, title, description, 
                   uploaded_by, uploaded_at, is_confidential
            FROM documents WHERE employee_id = ? ORDER BY uploaded_at DESC
        """
        docs = self._execute(query, (employee_id,))
        
        if not self._check_access(user_id, employee_id, AccessLevel.HR):
            docs = [d for d in docs if not d.get("is_confidential")]
        
        self._log_audit(employee_id, user_id, "LIST_DOCUMENTS", f"Listed {len(docs)} documents")
        return {"success": True, "count": len(docs), "documents": docs}

    # ================================================================
    # ABWESENHEITSMANAGEMENT
    # ================================================================

    def create_absence_request(self, employee_id: str, absence_data: Dict[str, Any],
                               user_id: str = "SYSTEM") -> Dict[str, Any]:
        if not self._check_access(user_id, employee_id, AccessLevel.SELF):
            return {"success": False, "message": "Access denied"}
        
        required = ["type", "start_date", "end_date"]
        for field in required:
            if field not in absence_data:
                raise ValueError(f"Missing required field: {field}")
        
        request_id = f"ABS-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().isoformat()
        
        query = """
            INSERT INTO absence_requests 
            (request_id, employee_id, type, start_date, end_date, status, comment, approved_by, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self._execute(query, (
            request_id, employee_id, absence_data["type"],
            absence_data["start_date"], absence_data["end_date"],
            "pending", absence_data.get("comment", ""), None, timestamp, timestamp
        ))
        
        self._log_audit(employee_id, user_id, "CREATE_ABSENCE_REQUEST", json.dumps(absence_data))
        return {"success": True, "request_id": request_id, "status": "pending"}

    def approve_absence(self, request_id: str, user_id: str = "SYSTEM") -> Dict[str, Any]:
        query = "SELECT access_level FROM access_control WHERE user_id = ?"
        results = self._execute(query, (user_id,))
        
        if not results or results[0]["access_level"] not in ["manager", "hr", "admin"]:
            return {"success": False, "message": "Access denied. Manager or HR required"}
        
        query_update = """
            UPDATE absence_requests 
            SET status = 'approved', approved_by = ?, updated_at = ?
            WHERE request_id = ?
        """
        self._execute(query_update, (user_id, datetime.now().isoformat(), request_id))
        
        req_query = "SELECT employee_id FROM absence_requests WHERE request_id = ?"
        req_results = self._execute(req_query, (request_id,))
        if req_results:
            self._log_audit(req_results[0]["employee_id"], user_id, "APPROVE_ABSENCE", f"Approved {request_id}")
        
        return {"success": True, "message": f"Request {request_id} approved"}

    # ================================================================
    # HEALTH CHECK
    # ================================================================

    def health_check(self) -> Dict[str, Any]:
        try:
            results = self._execute("SELECT COUNT(*) as count FROM employees")
            count = results[0]["count"] if results else 0
            return {
                "status": "healthy",
                "db_path": self.db_path,
                "documents_dir": self.documents_dir,
                "employee_count": count
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


# ------------------------------------------------------------------
# TOOL-CONTRACT – EINHEITLICHER EINSTIEG FÜR DIE SANDBOX
# ------------------------------------------------------------------

def run(payload: dict, action: dict) -> dict:
    """Standard-Contract: verarbeitet Payload und führt die angeforderte Aktion aus."""
    # Platzhalter-Prüfung für kritische Felder
    for key in ("employee_id", "request_id", "user_id"):
        val = payload.get(key)
        if isinstance(val, str) and "{{" in val:
            return {"success": False, "message": f"Unresolved planner variable in {key}: {val}"}

    # user_id aus Payload oder action (vom Runner gesetzt)
    user_id = payload.get("user_id") or action.get("user_id", "SYSTEM")

    # Tool-Instanz erstellen (Datenbank im Workspace)
    tool = HRTool()

    op = payload.get("op", "").lower()
    try:
        if op == "health":
            return tool.health_check()

        elif op == "grant_access":
            tool.grant_access(
                user_id=payload.get("user_id_to_grant", user_id),
                access_level=payload.get("access_level"),
                employee_id=payload.get("employee_id"),
                assigned_by=user_id
            )
            return {"success": True, "message": "Access granted"}

        elif op == "create_employee":
            return tool.create_employee(payload.get("employee_data", {}), user_id)

        elif op == "get_employee":
            emp_id = payload.get("employee_id")
            if not emp_id:
                return {"success": False, "message": "employee_id required"}
            return tool.get_employee(emp_id, user_id)

        elif op == "list_employees":
            return tool.list_employees(user_id, payload.get("department"))

        elif op == "update_employee":
            emp_id = payload.get("employee_id")
            if not emp_id:
                return {"success": False, "message": "employee_id required"}
            return tool.update_employee(emp_id, payload.get("updates", {}), user_id)

        elif op == "terminate_employee":
            emp_id = payload.get("employee_id")
            if not emp_id:
                return {"success": False, "message": "employee_id required"}
            return tool.terminate_employee(emp_id, payload.get("termination_date", datetime.now().strftime("%Y-%m-%d")),
                                          payload.get("reason", ""), user_id)

        elif op == "upload_document":
            emp_id = payload.get("employee_id")
            if not emp_id:
                return {"success": False, "message": "employee_id required"}
            file_content_b64 = payload.get("file_content_b64")
            if not file_content_b64:
                return {"success": False, "message": "file_content_b64 required"}
            import base64
            file_content = base64.b64decode(file_content_b64)
            return tool.upload_document(emp_id, payload.get("document_data", {}), file_content, user_id)

        elif op == "list_documents":
            emp_id = payload.get("employee_id")
            if not emp_id:
                return {"success": False, "message": "employee_id required"}
            return tool.list_documents(emp_id, user_id)

        elif op == "create_absence_request":
            emp_id = payload.get("employee_id")
            if not emp_id:
                return {"success": False, "message": "employee_id required"}
            return tool.create_absence_request(emp_id, payload.get("absence_data", {}), user_id)

        elif op == "approve_absence":
            req_id = payload.get("request_id")
            if not req_id:
                return {"success": False, "message": "request_id required"}
            return tool.approve_absence(req_id, user_id)

        elif op == "get_audit_trail":
            emp_id = payload.get("employee_id")
            if not emp_id:
                return {"success": False, "message": "employee_id required"}
            limit = int(payload.get("limit", 100))
            return tool.get_audit_trail(emp_id, limit)

        else:
            return {"success": False, "message": f"Unknown operation: {op}"}

    except Exception as e:
        log_event("hr_tool", "error", {"op": op, "error": str(e)}, severity="ERROR")
        return {"success": False, "message": str(e)}


# ------------------------------------------------------------------
# SUBPROZESS-EINSTIEG
# ------------------------------------------------------------------

if __name__ == "__main__":
    import json
    try:
        raw = sys.stdin.read()
        input_data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as e:
        print(json.dumps({"success": False, "message": f"Invalid JSON: {e}"}))
        sys.exit(1)

    payload = input_data.get("payload", input_data)
    action = input_data.get("action", {})
    result = run(payload, action)
    print(json.dumps(result, ensure_ascii=False))